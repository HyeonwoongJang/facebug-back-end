from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from post.models import Post, Comment, ConvertResult
from post.serializers import ConvertSerializer, PostCreateSerializer, PostListSerializer, CommentSerializer, CommentListSerializer
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import cv2


class PostListView(APIView):
    def get(self, request, user_id=None):
        """
        user_id가 없을 경우 모든 계시물을 Response 합니다.
        user_id가 있을 경우 특정 유저의 게시물을 Response 합니다.
        """
        if user_id is None:
            all_posts = Post.objects.all().order_by('-created_at')
            serializer = PostListSerializer(all_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            user_posts = Post.objects.filter(
                author=user_id).order_by('-created_at')
            serializer = PostListSerializer(user_posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ImageConvertView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """이미지를 받아 변환시킵니다."""
        serializer = ConvertSerializer(data=request.data)
        print("request.data : ", request.data)
        if serializer.is_valid():
            converted_data = serializer.save(owner=request.user)

            # 모델 로드
            detection_model_path = 'post/models/haarcascade_frontalface_default.xml'
            emotion_model_path = 'post/models/_mini_XCEPTION.102-0.66.hdf5'

            face_detection = cv2.CascadeClassifier(detection_model_path)
            emotion_classifier = load_model(emotion_model_path, compile=False)
            EMOTIONS = ["angry", "disgust", "scared",
                        "happy", "sad", "surprised", "neutral"]

            # 이미지 로드
            img = cv2.imread(f"media/{converted_data.original_image}")

            # 이미지 전처리하기
            h, w, c = img.shape  # h = 높이, w = 너비, c = 채널
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_detection.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

            # 표정 퍼센트 표시해 줄 캔버스 생성
            canvas = np.zeros((250, 300, 3), dtype="uint8")

            # 테스트
            # print(len(faces))

            if len(faces) > 0:
                faces = sorted(faces, reverse=True,
                               key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
                # print(faces)

                (fX, fY, fW, fH) = faces

                # Extract the ROI of the face from the grayscale image, resize it to a fixed 28x28 pixels, and then prepare
                # the ROI for classification via the CNN
                roi = gray[fY:fY + fH, fX:fX + fW]
                roi = cv2.resize(roi, (64, 64))
                roi = roi.astype("float") / 255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi, axis=0)

                preds = emotion_classifier.predict(roi)[0]
                emotion_probability = np.max(preds)
                label = EMOTIONS[preds.argmax()]
            else:
                print("인식된 얼굴이 없음.")

            # 감정 정보를 담을 리스트 생성
            text_dic = {}

            for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):
                # construct the label text
                text = "{}: {:.2f}%".format(emotion, prob * 100)
                text_dic["{}".format(emotion)] = "{:.2f}".format(prob * 100)

                # draw the label + probability bar on the canvas
                # emoji_face = feelings_faces[np.argmax(preds)]

                w = int(prob * 300)
                cv2.rectangle(canvas, (7, (i * 35) + 5),
                              (w, (i * 35) + 35), (0, 0, 255), -1)
                cv2.putText(canvas, text, (10, (i * 35) + 23),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45,
                            (255, 255, 255), 2)
                cv2.putText(img, label, (fX, fY - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                cv2.rectangle(img, (fX, fY), (fX + fW, fY + fH),
                              (0, 0, 255), 2)

            # 이미지 저장
            cv2.imwrite(
                f"media/{converted_data.converted_image}", img)

            # 넘겨줄 값 : 감정정보=text_list ... / 이미지= 경로 or 파일

            converted_data.result = text_dic
            converted_data.save()

            return Response({"message": "이미지 변환 완료", "owner_id": converted_data.owner.id, "owner_nickname" : converted_data.owner.nickname, "converted_result": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "이미지를 등록해주세요"}, status=status.HTTP_400_BAD_REQUEST)


class PostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """게시물을 생성합니다."""
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            
            data = ConvertResult.objects.get(id=request.data['content'])
            
            content = data.result
            post_img = data.converted_image
            
            return Response({"message": "게시물 생성 완료", "post_data" : serializer.data, "content" : content, "post_img" : str(post_img)}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        """post_id를 받아 특정 게시물을 삭제합니다."""
        post = get_object_or_404(Post, id=post_id)
        if request.user == post.author:
            post.delete()
            image = post.post_img
            image.delete()
            return Response({"message": "게시물 삭제 완료"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class PostLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        """like / unlike 기능입니다."""
        post = Post.objects.get(id=post_id)
        me = request.user
        if me in post.like.all():
            post.like.remove(me)
            return Response({"message": "unlike"}, status=status.HTTP_204_NO_CONTENT)
        else:
            post.like.add(me)
            return Response({"message": "like"}, status=status.HTTP_201_CREATED)


class CommentView(APIView):
    """
    comment_id가 없을 경우 댓글을 조회하거나 생성합니다.
    comment_id가 있을 경우 삭제합니다.
    """

    def post(self, request, post_id):
        """특정 게시물에 댓글을 생성합니다."""
        if request.user:
            serializer = CommentSerializer(data=request.data)
            # print(request.data)
            if serializer.is_valid():
                post = Post.objects.get(id=post_id)
                serializer.save(author=request.user, post=post)
                # print(serializer.data)
                return Response({"message": "댓글 등록 완료"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "로그인이 필요한 요청입니다."}, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, post_id):
        """특정 게시물에 작성된 모든 댓글을 불러옵니다."""
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post).order_by('-id')
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, post_id, comment_id):
        """특정 댓글을 삭제합니다."""
        if request.user:
            comment = Comment.objects.get(id=comment_id)
            if request.user == comment.author:
                comment.delete()
                return Response({"message": "댓글 삭제 완료"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "삭제 권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({"message": "로그인이 필요한 요청입니다."}, status=status.HTTP_401_UNAUTHORIZED)

#분류용 데이터 세트 준비
from sklearn.datasets import load_breast_cancer
cancer=load_breast_cancer()

#데이터 확인
print(cancer.data.shape, cancer.target.shape) #569개의 샘플과 각 샘플에는 30개의 특성이 있음. (569,30) (569,)

#데이터를 박스플롯으로 나타내기, 특성이 30개나 돼서 산점도로 나타내기 어려움.
import matplotlib.pyplot as plt
import numpy as np
plt.boxplot(cancer.data)
plt.xlabel('feature')
plt.ylabel('value')
plt.show()

#30개의 특성이 x축이고 그 값이 y축임.
#타깃의 고유한 값을 확인하기
print(np.unique(cancer.target, return_counts=True)) #(array[0,1], array[212,357]) 타깃의 고유한 값은 0(음성)과 1(양성)이고 음성의 수는 212개, 양성의 수는 357개


x=cancer.data
y=cancer.target

#훈련 데이터 세트를 훈련세트와 테스트세트로 나누어 사용하기
from sklearn.model_selection import train_test_split 
x_train, x_test, y_train, y_test = train_test_split(x,y, stratify=y, test_size=0.2, random_state=42)#훈련 데이터 세트를 훈련세트 75%, 테스트 세트 25%로 나누어주는 함수
#stratify=y는 훈련 데이터의 클래스 비율을 동일하게 만듦.
#test_size=0.2는 훈련 데이터 세트의 테스트 세트를 20%로 만듦.
#random_state=42는 실전에서는 필요없는데 여기서는 책이랑 똑같은 결과를 내기 위해 난수 초깃값 42를 씀.
print(x_train.shape, x_test.shape) #(455,30) (114,30) x가 455와 114로 4:1로 나누어짐을 확인
#양성 음성의 비율도 유지되는지 확인하기
print(np.unique(y_train, return_counts=True)) #(array([0,1]), array([170,285])) 훈련세트를 보니 170:285로 유지되어 있음.

#로지스틱 회귀 클래스 만들기
class LogisticNeuron:

  def __init__(self):
    self.w=None
    self.b=None

  def forpass(self,x):
    z=np.sum(x*self.w) + self.b # b+시그마i=1에서 n까지 w_i*x_i 형태의 방정식, np.sum은 array의 대응되는 모든 값을 계산 후 그 array의 모든 값을 더함.
    return z

  def backprop(self,x,err):
    w_grad = x*err
    b_grad = 1*err
    return w_grad, b_grad

  def fit(self, x, y, epochs=100):
    self.w = np.ones(x.shape[1]) #가중치를 1로 초기화함.
    self.b = 0 #절편을 0으로 초기화함.
    for i in range(epochs):
      for x_i, y_i, in zip(x,y):
        z=self.forpass(x_i) #정방향 계산
        a=self.activation(z) #활성화 함수 적용
        err= -(y_i - a)
        w_grad, b_grad = self.backprop(x_i, err) #역방향 계산
        self.w -= w_grad
        self.b -= b_grad

  #activation() 매서드
  def activation(self, z):
    a=1 / (1+np.exp(-z)) #시그모이드 함수 계산: 1/(1+e^(-z))
    return a

  #predict() 매서드
  def predict(self,x):
    z = [self.forpass(x_i) for x_i in x] #선형함수 적용, []안에 for문을 넣으면 새 리스트로 만들어줌.
    a = self.activation(np.array(z)) #활성화함수 적용, 리스트인 z를 np.array로 배열로 바꿔줌.
    return a > 0.5 #계단함수 적용

#훈련 시키기
neuron = LogisticNeuron()
neuron.fit(x_train, y_train)

neuron.predict(x_test[0:10])

#모델 정확도 파악하기 (테스트 세트 활용)
np.mean(neuron.predict(x_test) == y_test) #0.82어쩌고 나오는데 82% 정확도라는 거임.

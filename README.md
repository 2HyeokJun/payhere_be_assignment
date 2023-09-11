# ** PAYHERE_BACKEND_ASSIGNMENT **

## 1. 실행 방법
```
```
## 2. 구현 내용 설명
```
```
## 3. 코드에 대한 생각
* 바코드 정보는 숫자만 포함될까?
  https://www.keyence.co.kr/ss/products/auto_id/barcode_lecture/basic/barcode-types/
  에 따르면 CODE39, CODEBAR, CODE128 등은 알파벳과 특수문자 등도 포함된다고 한다.
  따라서 컬럼을 number가 아닌 varchar로 지정하기로 함.
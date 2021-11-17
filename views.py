from django.shortcuts import render
from result.models import student_details, student_marks
from result.serializers import studentserializer, student_mark_serializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework import status

# Create your views here.

class student_generic(generics.GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
	serializer_class = studentserializer
	queryset = student_details.objects.all()

	def get(self,request):
		return self.list(request)

	def post(self,request):
		return self.create(request)


@api_view([ 'POST'])
def student_mark_add(request,pk):
	try:
		if request.method == 'POST':
			serializer = student_mark_serializer(data=request.data)
			if serializer.is_valid():
				Marks = serializer.data['marks']
				if int(Marks)>=0 and int(Marks)<=100:
					student_marks.objects.create(id=pk,marks=Marks)
					return Response(serializer.data, status=status.HTTP_201_CREATED)
				else:
					return Response({"Marks":"Enter  value between 0 and 100" } )
			else:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	except:
		return Response({"value":"Enter valid value"})


class student_mark_view(APIView):
   
    def get_object(self, pk):
    	
        try:
            return student_marks.objects.get(id = pk)
        except student_marks.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = student_mark_serializer(snippet)
        return Response(serializer.data)


@api_view()
def Results(request,format = None):
	A_grade=[]
	B_grade=[]
	C_grade=[]
	D_grade=[]
	E_grade=[]
	fail=[]
	user=student_details.objects.count()
	marks = [user.marks for user in student_marks.objects.all()]
	for i in marks:
		if i >=91 and i <= 100:
			A_grade.append(i)
		elif i >=81 and i <=90:
			B_grade.append(i)
		elif i>=71 and i<=80:
			C_grade.append(i)
		elif i>=61 and i<=70:
			D_grade.append(i)
		elif i>=55 and i<=61:
			E_grade.append(i)
		else:
			fail.append(i)
	a_grade=len(A_grade)
	b_grade=len(B_grade)
	c_grade=len(C_grade)
	d_grade=len(D_grade)
	e_grade=len(E_grade)
	Fail=len(fail)
	distinction=(a_grade/user)*100
	first_class=((b_grade+c_grade)/user)*100
	Pass = ((user-Fail)/user)*100
	return Response({"The total number of students": user,
					"The number of students in each grade" : {
					"A Grade" :a_grade,
					"B Grade" :b_grade,
					"C Grade" :c_grade,
					"D Grade" :d_grade,
					"E Grade" :e_grade,
					"Fail"  : Fail
					},
					"Distinction %" : distinction,
					"First Class %" : first_class,
					"pass %" : Pass})
	
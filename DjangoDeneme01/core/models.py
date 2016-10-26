# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from django.db import models

from django.contrib.auth import models as auth_models

from django.db.models import ForeignKey
from django.db.models import CharField
from django.db.models import BooleanField
from django.db.models import DateField
from django.db.models import TimeField
from django.db.models import FloatField
from django.db.models import IntegerField
from django.db.models import DateTimeField
from django.db.models import TextField
from django.db.models import NullBooleanField


import django.utils.timezone as tz


class SoftDeleteManager(models.Manager):

	def get_queryset(self):
		return super(SoftDeleteManager, self).get_queryset().filter(is_deleted=False)


class Model(models.Model):

	objects = SoftDeleteManager()


	is_passive = NullBooleanField(null=True)
	is_deleted = NullBooleanField(null=True)
	create_ts = DateTimeField(null=True)
	update_ts = DateTimeField(null=True)
	delete_ts = DateTimeField(null=True)
	maked_passive_ts = DateTimeField(null=True)
	maked_active_ts = DateTimeField(null=True)


	class Meta:

		abstract = True



class UniqueObjectType(Model):

	name = CharField(max_length=55, null=True)
	description = CharField(max_length=255, null=True)


class UniqueObject(Model):

	type = ForeignKey(UniqueObjectType)



class ObjectEvent(Model):

	name = CharField(max_length=25, null=True)

	is_create = NullBooleanField(null=True)
	is_update = NullBooleanField(null=True)
	is_soft_delete = NullBooleanField(null=True)
	is_hard_delete = NullBooleanField(null=True)


class UniqueObjectHistory(Model):

	unique_object = ForeignKey(UniqueObject)
	event_type = ForeignKey(ObjectEvent)

	time = DateTimeField(null=True)

	old_value = TextField(null=True) # stored as json.
	new_value = TextField(null=True) # stored as json.



class BaseModel(Model):


	unique_object = ForeignKey(UniqueObject)



	def save(self, *args, **kwargs):

		is_new = None

		if not self.pk or kwargs.get('force_insert', False):

			is_new = True

		else:

			is_new = False



		class_name = str(self.__class__.__name__)
		unique_object_type = None
		now = tz.now()


		#print class_name










		try:

			unique_object_type = UniqueObjectType.objects.get(name=class_name)

		except:

			unique_object_type = UniqueObjectType()

			unique_object_type.name = class_name
			unique_object_type.description = class_name + " Object"

			unique_object_type.create_ts = now
			unique_object_type.update_ts = now
			unique_object_type.is_passive = False
			unique_object_type.is_deleted = False

			unique_object_type.save()







		unique_object = None


		event = None


		# old_value = None
		# new_value = None

		if is_new:

			unique_object = UniqueObject()

			unique_object.type = unique_object_type

			unique_object.create_ts = now

			unique_object.is_passive = False
			unique_object.is_deleted = False

			# old_value = {}

			self.create_ts = now
			self.is_passive = False
			self.is_deleted = False

			event = "create"

		elif not is_new:

			# old_self = self.__class__.objects.get(id=self.id)
			#
			# old_value = old_self.__dict__

			unique_object = self.unique_object

			event = "update"

		if is_new is None or event is None:

			pass # TODO : Raise Error

		else:


			unique_object.update_ts = now

			unique_object.save()



			self.unique_object = unique_object

			self.update_ts = now


			super(Model, self).save(*args, **kwargs)


			# new_value = self.__dict__
			#
			# event = ObjectEvent.objects.get(name=event)
			#
			# history_action = UniqueObjectHistory()
			#
			# history_action.unique_object = unique_object
			# history_action.event_type = event
			#
			# history_action.time = tz.now()
			#
			# history_action.old_value = old_value
			# history_action.new_value = new_value
			#
			# print history_action.__dict__
			#
			#
			# history_action.save()
			#
			# for i in UniqueObjectHistory.objects.all():
			#
			# 	print i.__dict__

	def delete(self, *args, **kwargs):

		# event = ObjectEvent.objects.get(name="hard_delete")
		#
		# history_action = UniqueObjectHistory()
		#
		# history_action.unique_object = self.unique_object
		# history_action.event_type = event
		#
		# history_action.time = tz.now()
		#
		# history_action.old_value = self.__dict__
		# history_action.new_value = {}
		#
		# history_action.save()

		self.is_deleted = True
		self.delete_ts = tz.now()

		self.save()


		# self.unique_object.delete()
		#
		# super(Model, self).delete(*args, **kwargs)



	class Meta:

		abstract = True



class Person(BaseModel):



	user = ForeignKey(auth_models.User, null=True)

	name = CharField(max_length=55, null=True)
	surname = CharField(max_length=55, null=True)

	tc_id = CharField(max_length=11, null=True)




class ShareAndExpireBase(BaseModel):

	is_inter_public = NullBooleanField(null=True)
	is_intra_public = NullBooleanField(null=True)
	is_private = NullBooleanField(null=True)
	is_expire = NullBooleanField(null=True)

	expire_time = DateTimeField(null=True)


	class Meta:

		abstract = True



class File(ShareAndExpireBase):

	name = CharField(max_length=55, null=True)
	path = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True)





class City(BaseModel):

	name = CharField(max_length=55, null=True)

class District(BaseModel):

	city = ForeignKey(City)
	name = CharField(max_length=55, null=True)





class AddressType(BaseModel):

	name = CharField(max_length=16, null=True)

class Address(BaseModel):

	person = ForeignKey(Person)
	name = CharField(max_length=20)
	type = ForeignKey(AddressType)
	district = ForeignKey(District)
	value = TextField(null=True)
	isDefault = NullBooleanField(null=True)






class PhoneNumberType(BaseModel):

	name = CharField(max_length=16, null=True)


class PhoneNumber(BaseModel):

	person = ForeignKey(Person)
	type = ForeignKey(PhoneNumberType)
	number = CharField(max_length=10, null=True)
	isDefault = NullBooleanField(null=True)
















class EducationLevel(BaseModel):

	name = CharField(max_length=25, null=True)



class EducationSection(BaseModel):

	level = ForeignKey(EducationLevel)
	name = CharField(max_length=25, null=True)








class Lesson(BaseModel):

	level = ForeignKey(EducationLevel)
	name = CharField(max_length=25, null=True)


class Subject(BaseModel):

	lesson = ForeignKey(Lesson)
	section = ForeignKey(EducationSection)
	name = CharField(max_length=55, null=True)





class Term(BaseModel):

	begin = DateField(null=True)
	end = DateField(null=True)
	isCurrent = NullBooleanField(null=True)

class SubTerm(BaseModel):

	term = ForeignKey(Term)
	name = CharField(max_length=25, null=True)
	end = DateField(null=True)










class Teacher(BaseModel):
	person = ForeignKey(Person)
	is_taxpayer = NullBooleanField(null=True)


class TTL(BaseModel): # TTL -> TeacherTeachableLesson

	teacher = ForeignKey(Teacher)
	lesson = ForeignKey(Lesson)


class Term_TTL(BaseModel): # TTL -> TeacherTeachableLesson

	ttl = ForeignKey(TTL)
	term = ForeignKey(Term)





class Student(BaseModel):

	person = ForeignKey(Person)


	mother_name_surname = CharField(max_length=25)
	father_name_surname = CharField(max_length=25)

	divorced_parent = NullBooleanField(null=True)

	orphan_father = NullBooleanField(null=True)
	orphan_mother = NullBooleanField(null=True)

	step_mother = NullBooleanField(null=True)
	step_father = NullBooleanField(null=True)

	sisters = IntegerField(null=True)
	brothers = IntegerField(null=True)
	elder_sisters = IntegerField(null=True)
	elder_brothers = IntegerField(null=True)

	step_sisters = IntegerField(null=True)
	step_brothers = IntegerField(null=True)
	step_elder_sisters = IntegerField(null=True)
	step_elder_brothers = IntegerField(null=True)


class TermStudent(BaseModel):

	student = ForeignKey(Student)
	teacher = ForeignKey(Teacher)
	term = ForeignKey(Term)
	school = CharField(max_length=60)
	section = ForeignKey(EducationSection)

	school_level = IntegerField(null=True)
	school_section = CharField(max_length=1)


class StudentLesson(BaseModel):

	student = ForeignKey(TermStudent)
	lesson = ForeignKey(Term_TTL)








class ParentType(BaseModel):

	name = CharField(max_length=25, null=True)

	mother = NullBooleanField(null=True)
	father = NullBooleanField(null=True)

	step_mother = NullBooleanField(null=True)
	step_father = NullBooleanField(null=True)

	elder_sisters = NullBooleanField(null=True)
	elder_brothers = NullBooleanField(null=True)

	step_elder_sisters = NullBooleanField(null=True)
	step_elder_brothers = NullBooleanField(null=True)

	uncle_father = NullBooleanField(null=True)
	uncle_mother = NullBooleanField(null=True)

	aunt_father = NullBooleanField(null=True)
	aunt_mother = NullBooleanField(null=True)

	uncle_in_law = NullBooleanField(null=True)
	aunt_in_law = NullBooleanField(null=True)

	grandpa_father = NullBooleanField(null=True)
	grandpa_mother = NullBooleanField(null=True)

	grandma_father = NullBooleanField(null=True)
	grandma_mother = NullBooleanField(null=True)

	other_relative = NullBooleanField(null=True)

	government = NullBooleanField(null=True)
	institution = NullBooleanField(null=True)
	school = NullBooleanField(null=True)

	other = NullBooleanField(null=True)




class Parent(BaseModel):
	person = ForeignKey(Person)
	teacher = ForeignKey(Teacher)
	comment = TextField(null=True)
	profession = TextField(max_length=25)
	where_work = TextField(max_length=50)





class ParentStudent(BaseModel):

	parent = ForeignKey(Parent)
	type = ForeignKey(ParentType)
	student = ForeignKey(TermStudent)
	comment = TextField(null=True)



class Schedule(BaseModel):

	date = DateField(null=True)
	begin_time = TimeField(null=True)
	end_time = TimeField(null=True)
	is_happened = NullBooleanField(null=True)
	comment = TextField(null=True)

	class Meta:

		abstract = True



class LectureRepetitive(BaseModel):

	from_date = DateField(null=True)
	end_date = DateField(null=True)
	day_of_week = IntegerField(null=True)
	repeat_of_week = IntegerField(null=True)
	lesson = ForeignKey(StudentLesson)
	begin_time = TimeField(null=True)
	end_time = TimeField(null=True)


class Lecture(Schedule):

	lesson = ForeignKey(StudentLesson)
	review_point = IntegerField(null=True)
	review_comment = TextField(null=True)
	comment_for_parent = TextField(null=True)
	is_repetitive = NullBooleanField(null=True)
	repetitive = ForeignKey(LectureRepetitive, null=True)




class PTASchedule(Schedule):

	teacher = ForeignKey(Teacher)
	parent = ForeignKey(ParentStudent)





class TaxType(BaseModel):

	name = CharField(max_length=25, null=True)
	rate = FloatField(null=True)




class Dealer(BaseModel):

	teacher = ForeignKey(Teacher)
	name = CharField(max_length=25, null=True)
	commission = FloatField(null=True) # Percent
	commission_is_tax_included = NullBooleanField(null=True)
	tax_type = ForeignKey(TaxType)



class Payment(BaseModel):

	lesson = ForeignKey(StudentLesson)
	dealer = ForeignKey(Dealer)

	issue_date = DateField(null=True)
	due_date = DateField(null=True)

	amount = FloatField(null=True)

	is_tax_included = NullBooleanField(null=True)
	tax_type = ForeignKey(TaxType)
	is_invoiced = NullBooleanField(null=True)

	is_clear = NullBooleanField(null=True)
	is_canceled = NullBooleanField(null=True)

	file = ForeignKey(File)


class Payer(BaseModel):

	name = CharField(max_length=25, null=True)

	is_student = NullBooleanField(null=True)
	is_parent = NullBooleanField(null=True)
	is_other = NullBooleanField(null=True)



class TransactionType(BaseModel):

	name = CharField(max_length=25, null=True) # Cash, Wire Transfer etc.




class Transaction(BaseModel):

	payment = ForeignKey(Payment)
	type = ForeignKey(TransactionType)
	payer = ForeignKey(Payer)
	date = DateField(null=True)
	amount = FloatField(null=True) # TL
	commission = FloatField(null=True) # TL
	tax = FloatField(null=True) # TL

	file = ForeignKey(File)




class HomeWorkType(BaseModel):

	teacher = ForeignKey(Teacher)
	name = CharField(max_length=25, null=True)
	comment = TextField(null=True)



class HomeWork(BaseModel):

	lecture = ForeignKey(Lecture)
	type = ForeignKey(HomeWorkType)
	dead_line = DateTimeField(null=True)
	review_day = DateField(null=True)
	comment = TextField(null=True)
	is_finished_in_time = NullBooleanField(null=True)
	is_finished_correctly = NullBooleanField(null=True)
	review_point = IntegerField(null=True)
	review_comment = TextField(null=True)
	comment_for_parent = TextField(null=True)


class HomeWorkFile(BaseModel):

	home_work = ForeignKey(HomeWork)
	file = ForeignKey(File)





class ProgressReview(BaseModel):

	lesson = ForeignKey(StudentLesson)
	begin = DateField(null=True)
	end = DateField(null=True)
	point = IntegerField(null=True)
	comment = TextField(null=True)
	comment_for_parent = TextField(null=True)





class ExamType(BaseModel):

	name = CharField(max_length=25, null=True)


class Exam(BaseModel):

	type = ForeignKey(ExamType)


	total_questions = IntegerField(null=True)

	correct_answers = IntegerField(null=True)
	wrong_answers = IntegerField(null=True)

	review_point = IntegerField(null=True)

	student_comment = TextField(null=True)

	class Meta:

		abstract  = True




class TeacherExam(Exam):

	lesson = ForeignKey(StudentLesson)

	comment = TextField(null=True)

	review_comment = TextField(null=True)

	comment_for_parent = TextField(null=True)


	begin = DateTimeField(null=True)
	end = DateTimeField(null=True)





class TeacherExamSubject(BaseModel):

	exam = ForeignKey(TeacherExam)
	subject = ForeignKey(Subject)
	comment = TextField(null=True)







class SchoolExam(Exam):

	student = ForeignKey(TermStudent)
	lesson = ForeignKey(Lesson)

	date = DateField(null=True)


class OtherExam(Exam):

	student = ForeignKey(TermStudent)
	lesson = ForeignKey(Lesson)

	date = DateField(null=True)

	description = TextField(null=True)







class ExamInstitution(BaseModel):

	name = CharField(max_length=55, null=True)
	short_name = CharField(max_length=8, null=True)


	is_osym = NullBooleanField(null=True)
	is_meb = NullBooleanField(null=True)

	is_tubitak = NullBooleanField(null=True)

	is_sat = NullBooleanField(null=True)

	is_other = NullBooleanField(null=True)





class BigExamType(BaseModel):

	name = CharField(max_length=55, null=True)
	short_name = CharField(max_length=8, null=True)

	institution = ForeignKey(ExamInstitution)

	education_level = ForeignKey(EducationSection)

	have_sub_exams = NullBooleanField(null=True)




class BigExam(BaseModel): # BE = Big Exam

	type = ForeignKey(BigExamType)
	term = ForeignKey(Term)

	begin = DateTimeField(null=True)
	end = DateTimeField(null=True)



class BE_Lesson(BaseModel): # BE = Big Exam

	exam = ForeignKey(BigExam)
	lesson = ForeignKey(Lesson)
	total_questions = IntegerField(null=True)



class BE_SubExam(BaseModel): # BE = Big Exam - BESE = Big Exam Sub Exam

	exam = ForeignKey(BigExam)

	begin = DateTimeField(null=True)
	end = DateTimeField(null=True)



class BESE_Lesson(BaseModel): # BESE = Big Exam Sub Exam

	exam = ForeignKey(BE_SubExam)
	lesson = ForeignKey(BE_Lesson)





class StudentBigExamInfoBase(BaseModel):

	student = ForeignKey(TermStudent)

	will_take = NullBooleanField(null=True)
	have_taked = NullBooleanField(null=True)

	exit_earlier = NullBooleanField(null=True)

	teacher_comment = TextField(null=True)
	student_comment = TextField(null=True)


	class Meta:

		abstract = True


class Student_BE_Info(StudentBigExamInfoBase): #  BE = Big Exam

	exam = ForeignKey(BigExam)





class Student_BESE_Info(StudentBigExamInfoBase): #  BESE = Big Exam Sub Exam

	exam = ForeignKey(BE_SubExam)





class Student_BE_Result(BaseModel):

	student = ForeignKey(TermStudent)
	lesson = ForeignKey(BE_Lesson)

	correct_answers = IntegerField(null=True)
	wrong_answers = IntegerField(null=True)

	teacher_comment = TextField(null=True)
	student_comment = TextField(null=True)




class TeacherReviewModel(BaseModel):

	teacher = ForeignKey(Teacher)
	stars = IntegerField(null=True)
	comment = TextField(null=True)


	class Meta:

		abstract = True



class ParentTeacherReview(TeacherReviewModel):

	parent = ForeignKey(Parent)



class StudentTeacherReview(TeacherReviewModel):

	student = ForeignKey(TermStudent)










class OtomationFileType(BaseModel):

	name = CharField(max_length=25, null=True)



class OtomationFile(BaseModel):

	type = ForeignKey(OtomationFileType)
	file = ForeignKey(File)






class TeacherFileType(BaseModel):

	teacher = ForeignKey(Teacher)
	name = CharField(max_length=25, null=True)



class TeacherFile(BaseModel):

	type = ForeignKey(OtomationFileType)
	file = ForeignKey(File)




class StudentFile(BaseModel):

	student = ForeignKey(Student)
	file = ForeignKey(File)



class ParentFile(BaseModel):

	parent = ForeignKey(Parent)
	file = ForeignKey(File)






class Message(BaseModel):

	sender = ForeignKey(Person, related_name='send_person_for_message')
	receiver = ForeignKey(Person,  related_name='receiver_person_for_message')

	send_time = DateTimeField(null=True)
	read_time = DateTimeField(null=True)

	is_deleted_sender = NullBooleanField(null=True) # These is not soft or hard delete. These is only hide message from Sender
	is_deleted_receiver = NullBooleanField(null=True) # These is not soft or hard delete. These is only hide message from Receiver

	is_read = NullBooleanField(null=True) # Is message read by receiver

	message = TextField(null=True)




class MessageAttachment(BaseModel):

	message = ForeignKey(Message)
	file = ForeignKey(File)








class SharedFile(BaseModel):

	file = ForeignKey(File)
	shared_with = ForeignKey(Person)

	is_expire = NullBooleanField(null=True)

	expire_time = DateTimeField(null=True)






class Article(ShareAndExpireBase):


	lesson = ForeignKey(TTL)

	is_published = NullBooleanField(null=True)
	publish_time = DateTimeField(null=True)



class ArticleInteraction(BaseModel):


	article = ForeignKey(Article)
	student = ForeignKey(Student)


	class Meta:

		abstract = True



class ArticleComment(ArticleInteraction):

	comment = TextField(null=True)


class ArticleStar(ArticleInteraction):

	star = IntegerField(null=True)


class ArticleLike(ArticleInteraction):

	like = NullBooleanField(null=True)


class ArticleUnLike(ArticleInteraction):

	un_like = NullBooleanField(null=True)




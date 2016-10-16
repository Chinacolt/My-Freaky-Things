import copy

class Element():

	def __init__(self):

		self.__elements = []
		self.__parent = None
		self.__tag = self.__class__.__name__.lower()


	def __racialize(self, obj=None):

		if obj == None:
			obj = self

		cls = obj.__class__
		base = cls.__base__

		while base is not object:

			cls = base
			base = base.__base__

		return cls



	def __checkImplementation(self, other):

		self_race = self.__racialize()
		other_race = self.__racialize(other)

		rule1 = self_race == other_race and self_race == Element
		rule2 = self_race == Element and other_race == "".__class__
		rule3 = self_race == "".__class__ and Element
		rule4 = self is not other

		if (rule1 or rule2 or rule3) and rule4:

			return True

		else:

			return False


	def __isFluid(self):

		if self.__class__ == Element:
			return True
		else:
			return False



	def __hasParent(self):

		if self.__parent is not None:
			return True
		else:
			return False


	def __str__(self):

		return "<" + self.__tag + "/>"


	def __iter__(self):

		for item in self.__elements:

			yield item


	def __len__(self):

		return len(self.__elements)



	def __getitem__(self, item):

		if type(item) == type(73):

			if item < len(self.__elements):

				return self.__elements[item]

			else:

				raise IndexError



		else:

			raise TypeError



	def __add__(self, other):

		if self.__checkImplementation(other):


			new = None

			if self.__isFluid():

				new = self

			else:

				new = Element()
				self.__parent = new
				new.__elements.append(self)




			if type(other) == type(""):

				new.__elements.append(other)

			elif other.__isFluid():

				for element in other:

					if type(element) is not type(""):
						element.__parent = new

					new.__elements.append(element)


			else:

				other.__parent = new
				new.__elements.append(other)


			return new


		else:

			return NotImplemented



	def __radd__(self, other):

		new = Element()
		new.__elements.append(other)
		other = new

		return other + self



	def __lt__(self, other):

		if self.__checkImplementation(other):


			if self.__isFluid():

				return NotImplemented

			elif type(other) is type(""):

				other.__parent = self
				self.__elements.append(other)

			elif other.__isFluid():

				for element in other:

					element.__parent = self
					self.__elements.append(element)

			else:

				other.__parent = self
				self.__elements.append(other)


			return self


		else:

			return NotImplemented


	def __gt__(self, other):

		return other < self




	def render(self):


		rtn = []


		rtn.append("<")
		rtn.append(self.__tag)

		for attr in self.__dict__:
			attr = str(attr)
			if attr.startswith("_Element__"):
				continue
			if not attr.startswith("__"):
				continue

			rtn.append(" ")
			rtn.append(attr[2:])
			rtn.append("=")
			rtn.append("\"")
			rtn.append(self.__dict__[attr])
			rtn.append("\"")

		rtn.append(">")


		for element in self.__elements:

			if type(element) == type(""):

				rtn.append(element)

			else:

				rtn.append(element.render())


		rtn.append("</")
		rtn.append(self.__tag)
		rtn.append(">")

		return "".join(rtn)








	def __getattr__(self, attr):

		attr = str(attr).lower()

		if attr == "parent":

			def getter():

				return self.__parent

			return getter

		real_attr = "_" + attr

		if attr.startswith("_Element__"):

			raise SyntaxError

		elif attr.startswith("__"):

			if attr in self.__dict__.keys():

				return self.__dict__[real_attr]


		elif not attr.startswith("_"):

			raise SyntaxError



		def setter(value=None):

			if value is not None:

				if type(value) in [type("3.14"), type(3), type(3.14), type([])]:

					if type(value) is type([]):

						for item in value:

							if not type(item) in [type("3.14"), type(3), type(3.14)]:

								raise ValueError

						value = " ".join(value)

					else:

						value = str(value)

					self.__dict__[real_attr] = value

				else:

					raise ValueError

				return self

			else:

				if "_" + attr in self.__dict__.keys():

					return self.__dict__[real_attr]

				else:

					raise AttributeError

		return setter




































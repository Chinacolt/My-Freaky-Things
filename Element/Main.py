
from Element import Element

class div(Element): pass
class img(Element): pass
class a(Element): pass



x = div()
y = a()


x = y + a()._href("elemanlar 1") + a()._href("elemanlar 2")

y._href("emre")

print(x.render())

x[0]._href("denemecibaba")

print(x.render())









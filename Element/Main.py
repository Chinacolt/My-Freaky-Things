
import copy

from Element import Element

class div(Element): pass
class img(Element): pass
class a(Element): pass


kkk = div()._class("box box-solid")

kkk < a()._href("emre.cintay.com") < div()._class("image thumbnail soft") < img()._src("emre.cintay.com/images/profile.png")

print(kkk.render())




# Documentation:
# https://github.com/Microsoft/xlang/tree/master/src/package/pywinrt/projection/

import winrt.windows.foundation as wf
u = wf.Uri("https://github.com/")
u2 = u.combine_uri("Microsoft/xlang/tree/master/src/tool/python")
print(str(u2))
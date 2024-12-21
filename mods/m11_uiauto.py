import uiautomation as auto
import os

try:
    import m03_windows as wnd
except ModuleNotFoundError:
    from . import m03_windows as wnd


def GetSelectFilePath(p_hwnd):
    res = []
    with auto.UIAutomationInitializerInThread(debug=False):
        openWnd = auto.ControlFromHandle(p_hwnd)

        for c, d in auto.WalkControl(openWnd, False, 8):
            if c.ControlTypeName == 'ToolBarControl':
                if c.AutomationId == '1001':
                    path_ = c.Name.split(' ', maxsplit=1)[1]
                    print('path', path_)
                    break
        else:
            raise ValueError('no ToolBarControl')

        ListControl = openWnd.ListControl()
        for c, d in auto.WalkControl(ListControl, False, 2):
            if c.ControlTypeName == 'ListItemControl':
                if c.GetSelectionItemPattern().IsSelected:
                    res.append(os.path.join(path_, c.Name))
    return res


def GetProcessFileName(p_hwnd):
    pid = wnd.GetWindowThreadProcessId(p_hwnd)
    hp = wnd.OpenProcess(wnd.PROCESS_QUERY_INFORMATION | wnd.PROCESS_VM_READ, False, pid)
    res = wnd.GetProcessFileName(hp)
    wnd.CloseHandle(hp)
    return res


if __name__ == '__main__':
    print(GetSelectFilePath(9307040))
    print(GetProcessFileName(9307040))

import uiautomation as auto
import os

try:
    import m03_windows as wnd
except ModuleNotFoundError:
    from . import m03_windows as wnd

import comtypes
import comtypes.client


def get_selected_paths_from_explorer_hwnd(p_hwnd: int) -> list[str]:
    """
    传入资源管理器窗口句柄 p_hwnd (int)，返回当前选中项的完整路径列表。
    注意：像“此电脑/控制面板/库”等虚拟项可能不是磁盘路径。
    """
    # comtypes.CoInitialize()  # 确保当前线程已初始化 COM（建议在主线程/STA）

    shell = comtypes.client.CreateObject("Shell.Application", dynamic=True)
    wins = shell.Windows()

    # comtypes 下更稳的遍历方式：Count + Item(i)
    try:
        count = int(wins.Count)
    except Exception:
        count = 0

    for i in range(count):
        try:
            w = wins.Item(i)
            if int(w.HWND) != int(p_hwnd):
                continue

            doc = w.Document  # IShellFolderViewDual2（资源管理器视图）
            items = doc.SelectedItems()
            n = int(items.Count)
            return [items.Item(j).Path for j in range(n)]
        except Exception:
            continue

    return []


def GetSelectFilePath(p_hwnd):
    res = []
    with auto.UIAutomationInitializerInThread(debug=False):
        return get_selected_paths_from_explorer_hwnd(p_hwnd)

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
    print(GetSelectFilePath(724394))
    print(GetProcessFileName(724394))

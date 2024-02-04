import pcbnew
import json
import wx
import sys
import traceback

HOLE_REF_PREFIX = 'H'
HOLE_REF_OFFSET = 1

def __get_mounting_holes(pcb_file):
    active = False

    for line in open(pcb_file, encoding="utf-8"):
        line = line.strip(" ()\n")
        if line.startswith("footprint"):
            if "MountingHole" in line:
                active = True

        if line.startswith("at") and active:
            parts = line.split(" ")
            x = float(parts[1])
            y = float(parts[2])
            
            yield (x, y)
            active = False

def place_drills(pcb_file):
    holes = list(__get_mounting_holes(pcb_file))
    board = pcbnew.GetBoard()
    msgs = []

    for i, pos in enumerate(holes):
        ref = f"{HOLE_REF_PREFIX}{i+HOLE_REF_OFFSET}"
        hole = board.FindFootprintByReference(ref)
        if hole is not None:
            hole.SetPosition(pcbnew.VECTOR2I_MM(*pos))
        else:
            msgs.append(f"No suitable hole in PCB, make sure that you have enough hole footprints and assigned all references! ({pos})")
    return msgs


class DrillPlacer(pcbnew.ActionPlugin):
    def defaults(self):
        self.name = 'Drill placer'
        self.category = 'Modify PCB'
        self.description = 'Align drills with another PCB'
        self.__version__ = '0.1.0'

    @property
    def version(self):
        return self.__version__

    def Run(self):
        self.__gui()

    def __gui(self):
        window_size = (800, 600)
        border = 10
        params = {"pcb_file": ""}

        class FilePanel(wx.Panel):
            def __init__(self, parent):
                def filepath_handler(_):
                    params["pcb_file"] = filepath_textbox.GetValue()

                def button_handler(_):
                    dialog = wx.FileDialog(None, 'Select a file', '', '', 'KiCAD PCB file|*.kicad_pcb', wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
                    if dialog.ShowModal() == wx.ID_OK:
                        filepath_textbox.SetValue(dialog.GetPath())
                    else:
                        filepath_textbox.SetValue("")

                super(FilePanel, self).__init__(parent, wx.ID_ANY)

                text = wx.StaticText(self, wx.ID_ANY, 'PCB file:')

                filepath_textbox = wx.TextCtrl(self, wx.ID_ANY)
                filepath_textbox.SetValue(params['pcb_file'])
                filepath_textbox.Bind(wx.EVT_TEXT, filepath_handler)

                button = wx.Button(self, wx.ID_ANY, 'Select')
                button.Bind(wx.EVT_BUTTON, button_handler)

                layout = wx.BoxSizer(wx.HORIZONTAL)
                layout.Add(text, flag=wx.ALIGN_CENTER)
                layout.Add(filepath_textbox, proportion=1, flag=wx.ALIGN_CENTER | wx.LEFT, border=border)
                layout.Add(button, flag=wx.ALIGN_CENTER | wx.LEFT, border=border)
                self.SetSizer(layout)


        class RunPanel(wx.Panel):
            def __init__(self, parent, top_frame):
                def button_run_handler(_):
                    print("Running Drill Placer")
                    try:
                        msgs = place_drills(params["pcb_file"])
                        if len(msgs) > 0:
                            wx.MessageBox('\n'.join(msgs), 'Warning', style=wx.OK | wx.ICON_WARNING)
                        top_frame.Close(True)
                    except Exception:
                        t, v, tb = sys.exc_info()
                        print(traceback.format_exception(t, v, tb))
                        wx.MessageBox('\n'.join(traceback.format_exception(t, v, tb)),
                                      'Execution failed', style=wx.OK | wx.ICON_ERROR)
                    finally:
                        return

                super(RunPanel, self).__init__(parent, wx.ID_ANY)
                button = wx.Button(self, wx.ID_ANY, 'Run')
                button.Bind(wx.EVT_BUTTON, button_run_handler)

                layout = wx.BoxSizer(wx.VERTICAL)
                layout.Add(button, 0, wx.GROW)
                self.SetSizer(layout)


        class TopFrame(wx.Frame):
            def __init__(self, title):
                super(TopFrame, self).__init__(None, wx.ID_ANY, title, size=window_size)

                root_panel = wx.Panel(self, wx.ID_ANY)

                file_panel = FilePanel(root_panel)
                run_panel = RunPanel(root_panel, self)

                root_layout = wx.BoxSizer(wx.VERTICAL)
                root_layout.Add(file_panel, 0, wx.GROW | wx.ALL, border=border)
                root_layout.Add(run_panel, 0, wx.GROW | wx.ALL, border=border)

                root_panel.SetSizer(root_layout)
                root_layout.Fit(root_panel)

        frame = TopFrame("Drill Placer")
        frame.Center()
        frame.Show()


DrillPlacer().register()

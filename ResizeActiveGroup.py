import sublime_plugin
import time
from copy import deepcopy


class ResizeActiveGroup(sublime_plugin.EventListener):
    def __init__(self):
        self.col_times  = []
    # based on the active group we calculate the cols/rows array
    def get_big(self, arr, activeGroup):
        return [arr[0], arr[1] if (activeGroup == 1) ^ (arr[1] > 0.5) else 1 - arr[1], arr[2]]

    # called when a different view is activated
    def on_activated(self, view):
        
        window = view.window()
        if window:
            activeGroup = window.active_group()
            oldLayout = window.get_layout()
            newLayout = deepcopy(oldLayout)

            print repr(newLayout) + '| ' + repr(activeGroup)
            
            # 2 cells
            if len(oldLayout["cells"]) == 2:
                # Columns: 2
                if len(oldLayout["rows"]) == 2:
                    newLayout["cols"] = self.get_big(oldLayout["cols"], activeGroup)
                # Rows: 2
                else:
                    newLayout["rows"] = self.get_big(oldLayout["rows"], activeGroup)

            # 4 cells
            elif len(oldLayout["cells"]) == 4:
                # Grid: 4
                if len(oldLayout["rows"]) == 3 and len(oldLayout["cols"]) == 3:
                    if activeGroup == 0:
                        newLayout["cols"] = self.get_big(oldLayout["cols"], activeGroup)
                        newLayout["rows"] = self.get_big(oldLayout["rows"], activeGroup)
                    elif activeGroup == 1:
                        newLayout["cols"] = self.get_big(oldLayout["cols"], activeGroup)
                        newLayout["rows"] = self.get_big(oldLayout["rows"], activeGroup - 1)
                    elif activeGroup == 2:
                        newLayout["cols"] = self.get_big(oldLayout["cols"], activeGroup - 2)
                        newLayout["rows"] = self.get_big(oldLayout["rows"], activeGroup - 1)
                    elif activeGroup == 3:
                        newLayout["cols"] = self.get_big(oldLayout["cols"], activeGroup - 2)
                        newLayout["rows"] = self.get_big(oldLayout["rows"], activeGroup - 2)


            # 3 cols/cells? not sure how it works
            elif len(oldLayout["cells"]) == 3 and len(oldLayout["cols"]) == 4:
                widths = []
                for i in xrange(len(oldLayout["cols"])-1):
                    widths += [oldLayout["cols"][i+1]-oldLayout["cols"][i]]
                widths = sorted(widths)
                w2 = [0 for i in xrange(len(widths))]


                for i in xrange(len(oldLayout["cols"])-len(self.col_times)-1):
                    self.col_times += [0];

                self.col_times[activeGroup] = time.time()
                order = sorted(zip(xrange(len(self.col_times)),self.col_times), key=lambda value:value[1])
                order = [o[0] for o in order]

                for i in xrange(len(widths)):
                    print i
                    w2[order[i]] = widths[i]

                print repr(widths)
                print repr(w2)
                print repr(order)
                left = 0
                for i in xrange(len(w2)):
                    left += w2[i]
                    newLayout["cols"][i+1] = left;
                print repr(newLayout["cols"])

            if oldLayout != newLayout:
                window.set_layout(newLayout)

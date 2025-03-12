from matplotlib import use,get_backend

gui_env = ['TKAgg','GTKAgg','Qt4Agg','WXAgg']

for gui in gui_env:
    try:
        print("testing", gui)
        use(gui, force=True)
        break
    except (ModuleNotFoundError,ValueError) as e:
        print (e)
        continue

print("Using:",get_backend())

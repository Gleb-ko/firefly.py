import firefly as ff
client = ff.Client("https://wincoll.fireflycloud.net/") # e.g. https://school.fireflycloud.net/
client.set_cookies(input("Cookies: "))

client.filter.sorting = ff.task.TaskFilter.Sorting(
    column=ff.task.TaskFilter.Sorting.Column.DUE_DATE,
    order=ff.task.TaskFilter.Sorting.Order.DESCENDING
)
# client.filter.completion_status = ff.task.TaskFilter.CompletionStatus.TO_DO
client.filter.page_size = 2
def on_update(page,page_size,val):
    print(val,page)
client._get_tasks(page=0)
for task in client.tasks:
    print("#########################")
    print(task.title,"-",task.setter.name,"-",task.student.name)
    print("[",task.id,"]\n")
    print(task.description)
    print()

client.tasks[0].toggle_done()
client.tasks[0].send_comment("Test")
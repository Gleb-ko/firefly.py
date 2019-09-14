import firefly as ff
client = ff.Client(input("Base URL of firefly: ")) # e.g. https://school.fireflycloud.net/
client.set_cookies(input("Cookies: "))

client.filter.sorting = ff.task.TaskFilter.Sorting(
    order=ff.task.TaskFilter.Sorting.Order.DESCENDING
)
client._get_tasks()
print(client.tasks[6].title)

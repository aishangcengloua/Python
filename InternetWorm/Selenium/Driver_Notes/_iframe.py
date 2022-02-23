from selenium import webdriver
from time import sleep
from selenium.webdriver import ActionChains#导入动作链对应的类

bro = webdriver.Edge()
bro.get('https://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')

#如果定位的标签是存在于iframe标签之中则必须通过如下操作再进行标签定位
bro.switch_to.frame('iframeResult')#切换浏览器标签定位的作用域
div = bro.find_element_by_id('draggable')
print(div)

#动作链
action = ActionChains(bro)
#点击且长按指定的标签
action.click_and_hold(div)

for i in range(5) :
    # perform()表示立即执行动作链操作
    # move_by_offset(x, y)：x表示水平方向，y表示竖直方向
    action.move_by_offset(50, 0).perform()
    sleep(0.3)

#释放动作链
action.release()
bro.quit()

# coding: utf-8

# In[1]:


from uiautomator import device as driver
import numpy as np
import time
import os
import sys


# In[2]:


Height=1280
Width=720
all_of_list=[]
if os.path.isfile("db.npy"):
    all_of_list = np.load ("db.npy").tolist()

# In[3]:


def autoJob(tv,sleep_time,sum=6,click=True):
    count_click=0
    count=0
    drag_str='adb shell input swipe '+str(Width*0.5)+' '+str(Height*0.88)+' '+str(Width*0.5)+' '+str(Height*0.3)
    for _ in range(100):
        text_lists=driver(className='android.widget.TextView')
        try:
            for i in range(len(text_lists)):
                txt=text_lists[i].text
                if len(txt)>11 and txt not in all_of_list and count<sum:
                    driver(text=txt,className='android.widget.TextView').click()
                    #分享，收藏，评论
                    if click and count_click<2:
                        #分享
                        time.sleep(4)
                        driver.click(0.94*Width, 0.975*Height)
                        time.sleep(2)
                        driver(text="分享到学习强国").click()
                        time.sleep(2)
                        driver.press.back()
                        #收藏
                        driver.click(0.84*Width, 0.975*Height)
                        #评论
                        time.sleep(1)
                        driver(text="欢迎发表你的观点").click()
                        time.sleep(2)
                        os.system("adb shell am broadcast -a ADB_INPUT_TEXT --es msg '中国加油，武汉加油！'")
                        os.system("adb shell input keyevent 66")#不知道为什么输入一个回车，点击发布才有反应
                        time.sleep(2)
                        driver(text="发布").click()
                        count_click=count_click+1
                        '''
                        @liuzhijie443
                        #收藏
                        time.sleep(5)
                        driver.click(0.84*Width, 0.975*Height)
                        time.sleep(1)
                        driver.click(0.84*Width, 0.975*Height)
                        #删除发布的评论
                        time.sleep(2)
                        driver(text="删除").click()
                        time.sleep(2)
                        driver(text="确认").click()
                        '''
                    count=count+1
                    all_of_list.append(txt)
                    print("正在"+tv+"...",txt)
                    time.sleep(sleep_time)
                    driver.press.back()
        except BaseException:
            print("抛出异常，程序继续执行...")
        if count >=sum:
            break
        os.system(drag_str)


def watch_local():
    driver(text='北京').click()
    time.sleep(2)
    driver(text='北京卫视').click()
    print("观看本地频道...")
    time.sleep(20)
    print("本地频道结束")
    driver.press.back()
# In[4]:


#阅读文章,阅读6个文章，每个文章停留130秒
def read_articles():
    time.sleep(2)
    #切换到要闻界面
    driver(text='北京').click()
    autoJob(tv="阅读文章",sleep_time=130)
    print("阅读文章结束")


# In[5]:


#观看视频,每个视频观看20秒，以及17分钟新闻联盟
def watch_video():
    time.sleep(2)
    #切换到电视台页面
    driver(resourceId="cn.xuexi.android:id/home_bottom_tab_button_contact").click()
    driver(text="联播频道").click()
    autoJob(tv="观看视频",sleep_time=20,click=False)
    driver(text="联播频道").click()
    
    news=None
    for v in driver(className='android.widget.TextView'):
        if "《新闻联播》" in v.text:
            news=v.text
            break
    driver(text=news).click()

    #100天后删除最早一天的记录
    text_list=np.array (all_of_list)
    
    if len(text_list)>2500:
        text_list = text_list[25:]
    #存储已看视频和文章
    np.save ('db.npy',text_list)
    
    print("正在观看新闻联播...")
    time.sleep(1050)
    driver.press('back')
    print("观看视频结束.")


# In[6]:

if __name__ == '__main__':
    #自动打开学习强国
    #os.system('adb shell am start cn.xuexi.android/com.alibaba.android.rimet.biz.SplashActivity')
    #屏幕高度
    Height=driver.info['displayHeight']
    Width=driver.info['displayWidth']
    #切换adb输入法
    os.system('adb shell ime set com.android.adbkeyboard/.AdbIME')
    watch_local()
    read_articles()
    watch_video()
    #切换回搜狗输入法
    #os.system('adb shell ime set com.sohu.inputmethod.sogou.meizu/com.sohu.inputmethod.sogou.SogouIME')
    #熄灭屏幕
    os.system('adb shell input keyevent 26')

# SIMU

时间驱动的 Python 仿真框架.

A time-driven simulation framework of Python


# 基本概念

在 **环境（Environment）** 中，若干个各种种类的 **仿真实体（Entity）** 按照自己的行为，在其中 **随时间（步进）** 和 **相互影响（互操作）** 而 **改变状态**。

---

## 环境（Environment）

环境是仿真运行的平台。
主要有以下功能：

* 管理仿真实体
  
  * 增加实体： add

  * 删除实体： remove

  * 查找实体： find

* 管理仿真过程

  * 步进（step）
  
    在仿真运行时，最为重要的概念和操作是 **步进** ：
  
    ```python
    """ 单次步进的伪代码 """

    def step(env):
        # 对象互操作
        for obj in objects:
            obj.access(others)

        # 对象步进
        for obj in objects:
            obj.step()

        # 实体和环境处理步进消息.
        for obj in objects:
            obj.on_step()
        env.on_step()
      
        # 时钟步进.
        clock.step()
    ```
  * 重置（reset）

  * 连续运行（run）
---

## 实体（Entity）

实体有属性:

* ID

  每个实体有全局唯一的 ID 号码作为标志.

* 名字 [可选]
  
  每个实体可以设置一个名字. 主要用来查找.

实体通过以下方式扩展功能:

* 步进消息处理函数列表：**step_events**

  步进消息，每执行一步后，将调用该实体的步进消息处理函数，处理某些操作.

  步进消息处理函数的原型如下：
  ``` python
  def on_event(obj : Entity):
      ...
  ```

  步进消息处理以列表方式保存. 实体可以顺序执行多个操作.


  ``` python
  obj = Entity()
  obj.step_events.append(lambda obj: ...)
  ```

* 步进动作处理函数列表：**step_handlers**
  
  每次步进时，实体**可以**通过步进动作处理函数来改变状态.

  步进动作处理函数的原型如下：
  ```python
  def step_handler(obj, time_info):
      ...
  ```

  步进动作处理函数列表的存在.
  
  有助于将对象的状态和动作进行分离.

* 互操作函数列表： **access_handlers**
  
  实体与其他实体的互操作，意味着该实体将根据其他对象的状态，设置自身的状态.

  互操作函数的原型如下：
  ```python
  def access_handler(self, other):
      ...
  ```

  互操作函数以列表方式保存. 实体可以顺序执行多个互操作.



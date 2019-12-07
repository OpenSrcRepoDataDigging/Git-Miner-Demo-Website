import os
import subprocess
import jpype




def test1():
    # 指定jar包位置, 或者.class文件
    jar_path = '/home/young/Desktop/Git Repo Miner/Git-Miner-Demo-Website/GitMiner-1.0-SNAPSHOT.jar'
    # JVM的路径位置
    JVM_path = jpype.getDefaultJVMPath()
    # 开启JVM，且指定jar包, 或者.class文件位置
    jpype.startJVM((JVM_path, jar_path))
    # 打印hello, word
    jpype.java.lang.System.out.println("hello World")
    # 引入java程序中的类.路径应该是项目中的package包路径.类名
    javaClass = jpype.JClass('MainDataGenerator')
    # 创建一个对象
    javaInstance = javaClass()
    # 执行类中的函数了
    res = javaInstance.generateNew(10, 20)
    print(res)
    # 关闭JVM
    jpype.shutdownJVM()

if __name__ == '__main__':
    jar_path = os.path.join(os.path.abspath('.'), 'GitMiner-1.0-SNAPSHOT.jar')

    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % jar_path)

    MainDataGenerator = jpype.JClass('LaunchFunction.MainDataGenerator')

    mdg = MainDataGenerator()

    res = mdg.generateNew("https://github.com/NJU-Trust/DailyPlan")

    print(res)

    jpype.shutdownJVM()

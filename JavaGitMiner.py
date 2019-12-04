import os
import jpype


class GitMiner():
	def __init__(self, jar_path = 'GitMiner-1.0-SNAPSHOT.jar') -> None:
		super().__init__()
		# 指定jar包位置, 或者.class文件
		self.jar_path = os.path.join(os.path.abspath('.'), jar_path)
		# 开启JVM，且指定jar包, 或者.class文件位置
		jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % self.jar_path)

	def git_clone(self, url):
		# 引入java程序中的类.路径应该是项目中的package包路径.类名
		MainDataGenerator = jpype.JClass('LaunchFunction.MainDataGenerator')
		# 创建一个对象
		mdg = MainDataGenerator()
		# 执行类中的函数了
		res = mdg.generateNew(url)
		print(res)
		return res


if __name__ == '__main__':
	git_miner = GitMiner()
	res = git_miner.git_clone(url="git@github.com:OpenSrcRepoDataMining/alluxio.git")
	print(res)

    



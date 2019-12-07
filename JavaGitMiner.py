import os
import jpype
from FrechetDistance import FrechetDistance
import repoDB_Options
import getpass


class GitMiner():
	def __init__(self, jar_path = 'GitMiner-1.0-SNAPSHOT.jar') -> None:
		super().__init__()
		# 指定jar包位置, 或者.class文件
		self.jar_path = os.path.join(os.path.abspath('.'), jar_path)
		# 开启JVM，且指定jar包, 或者.class文件位置
		jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % self.jar_path)
		self.frechet = FrechetDistance()

	def get_path_prefix_from_url(self,url):
		repo_name = ""
		stringlist = url.split("/")
		tmp_name = stringlist[len(stringlist) - 1]
		tmp_name = tmp_name.split('.')
		repo_name = tmp_name[0]
		print("this repo_name is" + repo_name)
		db = repoDB_Options.repoDB_Options()
		prefix = str(db.get_repo_path_prefix(repo_name))
		return prefix

	def git_clone(self, url):
		# 引入java程序中的类.路径应该是项目中的package包路径.类名
		MainDataGenerator = jpype.JClass('LaunchFunction.MainDataGenerator')
		# 创建一个对象
		mdg = MainDataGenerator()
		# 执行类中的函数了
		res = mdg.generateNew(url)
		print(res)
		path_prefix = self.get_path_prefix_from_url(url)
		self.frechet.get_frechet_distance(path_prefix)
		return res


if __name__ == '__main__':
	git_miner = GitMiner()
	#res = git_miner.git_clone(url="git@github.com:OpenSrcRepoDataMining/alluxio.git")
	res = git_miner.git_clone(url="git@github.com:njubigdata04/InvertedIndexWithHbase.git")
	print(res)

    



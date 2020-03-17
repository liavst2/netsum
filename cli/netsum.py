
import click
import time
from tools.fs import FsUtil

@click.group()
def main():
	pass


@main.command()
@click.option('--direction', '-d', default="out", help='Direction of internet data', type=click.Choice(['out', 'in']))
@click.option('--iface', '-i', default="wlp3s0", help='The interface to monitor')
def amount(direction, iface):
	"""
	Get amount of internet data - incoming or outgoing
	"""
	dir_ = "tx" if direction == "out" else "rx"
	gig = FsUtil.extract_int('/sys/class/net/' + iface + '/statistics/' + dir_ + '_bytes')
	print_msg = "Transmission" if direction == "out" else "Reception"
	print(print_msg + " amount so far is " + str(gig / (1024**2)) + " GB")


@main.command()
@click.option('--interval', '-d', default=0, help='Direction of internet data')
@click.option('--iface', '-i', default="wlp3s0", help='The interface to monitor')
def snapshot():
	pass


if __name__ == '__main__':
    main()
  


import click
import time
from tools.fs import FsUtil

@click.group()
def main(): pass


@main.command()
@click.option('--direction', '-d', default="out", help='Direction of internet data', type=click.Choice(['out', 'in']))
@click.option('--iface', '-i', default="wlp3s0", help='The interface to monitor')
def amount(direction, iface):
	"""
	Get amount of internet data so far - incoming or outgoing
	"""
	dir_, print_msg = ["tx", "Transmission"] if direction == "out" else ["rx", "Reception"]
	mb = FsUtil.extract_int('/sys/class/net/' + iface + '/statistics/' + dir_ + '_bytes')
	click.echo("{} amount so far is {} MB".format(print_msg, str(mb / (1024**2))))
	return mb


@main.command()
@click.option('--direction', '-d', default="out", help='Direction of internet data', type=click.Choice(['out', 'in']))
@click.option('--iface', '-i', default="wlp3s0", help='The interface to monitor')
@click.option('--seconds', '-s', default=0, help='The window size in seconds')
@click.pass_context
def record(ctx, direction, iface, seconds):
	"""
	Get amount of internet data in a fixed-sized seconds window - incoming or outgoing
	"""
	start = ctx.invoke(amount, direction=direction, iface=iface)
	time.sleep(seconds)
	end = ctx.invoke(amount, direction=direction, iface=iface)
	deltaMB = (end - start) / (1024**2)
	print_msg = "Transmission" if direction == "out" else "Reception"
	click.echo("In a {} seconds window, {} amount was {} MB".format(seconds, print_msg, deltaMB))
	return deltaMB


if __name__ == '__main__':
    main()
  

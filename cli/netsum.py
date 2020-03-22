
import click
import time
import sched
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
	click.echo(f"{print_msg} amount so far is {str(mb / (1024**2))} MB")
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
	click.echo(f"In a {seconds} seconds window, {print_msg} amount was {deltaMB} MB")
	return deltaMB


@main.command()
@click.option('--period', '-p', default="hourly", help='Send a periodic internet usage report to Email', type=click.Choice(['hourly', 'daily', 'weekly', 'monthly']))
@click.option('--direction', '-d', default="out", help='Direction of internet data', type=click.Choice(['out', 'in']))
@click.option('--iface', '-i', default="wlp3s0", help='The interface to monitor')
@click.option('--send_email', default=None, help='The Email from which the report is sent')
@click.option('--recv_email', default=None, help='The Email to send the report to')
@click.pass_context
def report(ctx, period, direction, iface, send_email, recv_email):
	"""
	Report amount of internet data to a given Email.
	"""
	def send(seconds):
		deltaMB = ctx.invoke(record, direction=direction, iface=iface, seconds=seconds)
		print(f"deltaMB is {deltaMB}")

	scheduler = sched.scheduler(time.time, time.sleep)
	dir_file = ('tx' if direction == "out" else 'rx') + "_bytes"
	period_as_seconds = 3 if period == "hourly" else 86400 if period == "daily" else 604800 if period == "weekly" else 2.628e+6
	scheduler.enter(period_as_seconds, 1, send, argument=(period_as_seconds,))
	scheduler.run()

if __name__ == '__main__':
    main()
  

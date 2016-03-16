from django.db import models
from django.contrib import admin
import colorsys, time

class LogEntry(models.Model):
	at = models.DateTimeField()
	submitted_by = models.IntegerField()
	trackable = models.ForeignKey('Trackable', related_name='+')

 	def __unicode__(self):
		return "%s on flight '%s' at %s" % (self.trackable.name, self.trackable.flight.name,self.at)

class Position(LogEntry):
	longitude = models.FloatField()
	latitude = models.FloatField()
	radius = models.FloatField()
	altitude = models.FloatField()
 
class Comment(LogEntry):
	text = models.TextField()

class Flight(models.Model):
	started = models.DateTimeField()
	aborted = models.DateTimeField(blank=True,null=True)
	completed = models.DateTimeField(blank=True,null=True)

	name = models.CharField(max_length=50)
	description = models.TextField(blank=True,null=True)

	last_updated = models.DateTimeField(blank=True,null=True)

	def __unicode__(self):
		return self.name
		
	def log_entries(self):
		"""returns a Manager containing all of the log entries associated with this flight"""
		return LogEntry.objects.filter(trackable__flight=self).order_by('-at')
		
	def is_flying(self):
		"""if any Trackables are in flight this returns True"""
		for trackable in self.trackables.all():
			if trackable.in_flight:
				return True
		return False
		
	def status(self):
		if self.aborted:
			return "Aborted"
		elif self.completed:
			return "Completed"
		elif self.is_flying:
			return "In Flight"
		elif self.started:
			return "Pre-Launch"
		return "Mystery!" # shouldn't happen?
			
class Trackable(models.Model):
	name = models.CharField(max_length=50)
	flight = models.ForeignKey('Flight', related_name='trackables')
	
	class Meta:
		ordering = ['name']	
	
	def __unicode__(self):
		return self.name

	def positions(self):
		return Position.objects.filter(trackable=self).order_by('-at')

	def current_position(self):
		try: 
			return self.positions().order_by('-at')[0]
		except:
			return None
			
	def start_position(self):
		try: 
			return self.positions().order_by('at')[0]
		except:
			return None

	def is_flying(self): # XXX this should be a field check probably since pre-launch altitude can be > 0
		return self.altitude > 0

	def html_colour(self):
		all_trackables = list(self.flight.trackables.all())
		our_position = float(all_trackables.index(self))
		rgb = colorsys.hsv_to_rgb(our_position / len(all_trackables), 1, 0.8)
		html_rgb = (rgb[0]*255, rgb[1]*255, rgb[2]*255)
		return '#%02x%02x%02x' % html_rgb

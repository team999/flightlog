from django import forms
from django.shortcuts import render_to_response
from django.http import Http404
from django.utils.html import escape
from django.utils.simplejson import dumps
from gmapi import maps
from gmapi.forms.widgets import GoogleMap
from main.models import * # XXX lazy!

class MapForm(forms.Form):
  map = forms.Field(widget=GoogleMap())

def flight(request, flight_id):
  try:
      flight = Flight.objects.get(pk=flight_id)
  except Flight.DoesNotExist:
      raise Http404

  gmap = maps.Map(opts = {
      'mapTypeId': maps.MapTypeId.TERRAIN,
      'zoom': 8,
      'mapTypeControlOptions': {
           'style': maps.MapTypeControlStyle.DROPDOWN_MENU
      },
  })

  context = {'form': MapForm(initial={'map': gmap}), 'flight': flight}
  return render_to_response('flight.html', context)

def stats(request, flight_id):
  try:
      flight = Flight.objects.get(pk=flight_id)
  except Flight.DoesNotExist:
      raise Http404

  context = {'flight': flight}
  return render_to_response('stats.html', context)      
      
def circles(request, flight_id):
  try:
      flight = Flight.objects.get(pk=flight_id)
  except Flight.DoesNotExist:
      raise Http404

  circles = []

  for trackable in flight.trackables.all():
    if trackable.start_position() and trackable.current_position() != trackable.start_position():
      marker = maps.Circle(opts={'fillColor': trackable.html_colour(), 'strokeColor': trackable.html_colour(), 'fillOpacity': 0.75 })
      marker.setRadius(trackable.current_position().radius)
      marker.setCenter(maps.LatLng(trackable.start_position().latitude, trackable.start_position().longitude))
      circles.append(marker)
    if trackable.current_position():
      marker = maps.Circle(opts={'fillColor': trackable.html_colour(), 'strokeColor': trackable.html_colour(), 'fillOpacity': 0.75 })
      marker.setRadius(trackable.current_position().radius)
      marker.setCenter(maps.LatLng(trackable.current_position().latitude, trackable.current_position().longitude))
      circles.append(marker)

  context = { 'json': dumps(circles, separators=(',', ':'))}
  return render_to_response('json.html', context)

def polylines(request, flight_id):
  try:
    flight = Flight.objects.get(pk=flight_id)
  except Flight.DoesNotExist:
    raise Http404
  
  polylines = []
  
  for trackable in flight.trackables.all():
    points = []
    for position in trackable.positions():    
      points.append(maps.LatLng(position.latitude, position.longitude))
    polyline = maps.Polyline(opts={'strokeColor': trackable.html_colour()})
    polyline.setPath(points)
    polylines.append(polyline)
    
  context = { 'json': dumps(polylines, separators=(',', ':'))}
  return render_to_response('json.html', context)

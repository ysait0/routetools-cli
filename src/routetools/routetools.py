#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import csv
import zipfile
import numpy
import xml.etree.ElementTree as ET
from geopy.distance import geodesic

class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'

class RouteTools:
  def __init__(self):
    pass

  def check_type(self, filepath):
    filename = os.path.basename(filepath)
    type_ = filename.split('.')[-1].upper()
    return type_

  def _parse(self, filepath):
    type_input = self.check_type(filepath)
    if type_input in ['CSV', 'GPX', 'KML', 'KMZ', 'TCX']:
      metadata, trackpoints, POI_list = globals()[type_input].parse(filepath)
    else:
      print(Color.RED + f"{type_input} is not supported yet" + Color.END, file=sys.stderr)
      sys.exit(1)
    return metadata, trackpoints, POI_list

  def parse(self, filepath):
    type_input = self.check_type(filepath)
    if type_input == 'CSV':
      print(Color.RED + f"{type_input} is not supported yet for base route file" + Color.END, file=sys.stderr)
      sys.exit(1)
    else:
      self.metadata, self.trackpoints, self.POI_list = self._parse(filepath)

  def add_poi(self, filepath):
    _, __, POI_list = self._parse(filepath)
    self.POI_list += POI_list

  def remove_poi(self):
    self.POI_list = []

  def build(self, type_output="TCX"):
    self.type_output = type_output
    if self.type_output in ['GPX', 'TCX']:
      root = globals()[self.type_output].build(self.metadata, self.trackpoints, self.POI_list)
    else:
      print(Color.RED + f"{type_output} is not supported yet" + Color.END, file=sys.stderr)
      sys.exit(1)
    self.tree = ET.ElementTree(root)

  def set_indent(self, indent=1):
    ET.indent(self.tree, ' '*indent)

  def dump(self, indent=1):
    self.set_indent(indent)
    ET.dump(self.tree)

  def write(self, filepath, indent=1):
    self.set_indent(indent)
    type_output = self.check_type(filepath)
    if type_output != self.type_output:
      print(Color.RED + f"Warning: output type is different\noutput type is set by --out-type (default: TCX) and now you chose {self.type_output}\nwhile output type assuming by output filename is {type_output}\nthere is no output file" + Color.END, file=sys.stderr)
      sys.exit(1)
    self.tree.write(filepath, encoding='UTF-8', xml_declaration=True)
    print(f"Wrote to: {filepath}", file=sys.stderr)

  def output_poi(self, filepath):
    if self.POI_list:
      with open(filepath, 'w') as f:
        writer = csv.writer(f)
        for POI in self.POI_list:
          writer.writerow([POI.latitude, POI.longitude, POI.name, POI.notes, POI.type_])
      print(f"Wrote to: {filepath}", file=sys.stderr)
    else:
      print(Color.RED + f"There are no POI to output" + Color.END, file=sys.stderr)
      sys.exit(1)

class Metadata:
  def __init__(self, name, type_=None):
    self.name  = name
    self.type_ = type_ if type_ else "Ride"

class Trackpoint:
  def __init__(self, latitude, longitude, elevation, distance=None):
    self.latitude  = latitude
    self.longitude = longitude
    self.coords    = [self.latitude, self.longitude]
    self.elevation = elevation
    self.distance  = distance

class POI:
  def __init__(self, latitude, longitude, name, notes=None, type_=None, symbol=None):
    self.latitude  = latitude
    self.longitude = longitude
    self.coords    = [self.latitude, self.longitude]
    self.name      = name
    self.notes     = notes
    self.type_     = type_
    self.symbol    = symbol

class CSV:
  def parse(filepath):
    POI_list = []
    with open(filepath, 'r') as f:
      lines = csv.reader(f)
      for line in lines:
        latitude = line[0]
        longitude = line[1]
        name = line[2]
        notes = line[3]
        try:
          type_ = line[4]
        except:
          type_ = None
        POI_list.append(POI(latitude, longitude, name, notes=notes, type_=type_))
    return None, None, POI_list 

class GPX:
  def parse(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    name = root.findtext('.//{*}metadata/{*}name')
    type_ = root.findtext('.//{*}trk/{*}type')
    metadata = Metadata(name=name, type_=type_)
    trackpoints = []
    for trkpt in root.findall('.//{*}trkpt'):
      latitude = trkpt.get('lat')
      longitude = trkpt.get('lon')
      elevation = trkpt.findtext('{*}ele')
      trackpoints.append(Trackpoint(latitude, longitude, elevation))
    POI_list = []
    for wpt in root.findall('.//{*}wpt'):
      latitude = wpt.get('lat')
      longitude = wpt.get('lon')
      name = wpt.findtext('{*}name')
      notes = wpt.findtext('{*}desc')
      type_ = wpt.findtext('{*}type')
      symbol = wpt.findtext('{*}sym')
      POI_list.append(POI(latitude=latitude, longitude=longitude, name=name, notes=notes, type_=type_, symbol=symbol))
    return metadata, trackpoints, POI_list

  def build(metadata, trackpoints, POI_list):
    root = ET.Element('gpx')
    root_metadata = ET.SubElement(root, 'metadata')
    ET.SubElement(root_metadata, 'name').text = metadata.name
    for poi in POI_list:
      wpt = ET.Element('wpt')
      wpt.set('lat', poi.latitude)
      wpt.set('lon', poi.longitude)
      ET.SubElement(wpt, 'name').text = poi.name
      ET.SubElement(wpt, 'desc').text = poi.notes
      ET.SubElement(wpt, 'sym').text = poi.symbol if poi.symbol else 'Flag'
      ET.SubElement(wpt, 'type').text = poi.type_ if poi.type_ else 'Flag'
      root.append(wpt)
    trk = ET.SubElement(root, 'trk')
    ET.SubElement(trk, 'name').text = metadata.name
    ET.SubElement(trk, 'type').text = metadata.type_
    trkseg = ET.SubElement(trk, 'trkseg')
    for trackpoint in trackpoints:
      trkpt = ET.Element('trkpt')
      trkpt.set('lat', trackpoint.latitude)
      trkpt.set('lon', trackpoint.longitude)
      ET.SubElement(trkpt, 'ele').text = trackpoint.elevation
      trkseg.append(trkpt)
    return root

class KML:
  def parse(filepath):
    if 'kmz' in filepath:
      zf = zipfile.ZipFile(filepath, 'r')
      for fn in zf.namelist():
        if fn.endswith('.kml'):
          content = zf.read(fn)
          root = ET.fromstring(content)
          break
    else:
      tree = ET.parse(filepath)
      root = tree.getroot()
    name = root.findtext('.//{*}Document/{*}name')
    metadata = Metadata(name=name)
    trackpoints = []
    POI_list = []
    for placemark in root.findall('.//{*}Placemark'):
      if placemark.find('{*}LineString'):
        wpts = [ i.strip().split(',') for i in placemark.find('{*}LineString/{*}coordinates').text.replace(' ', '').splitlines()]
        for wpt in wpts:
          if len(wpt) > 1:
            latitude = wpt[1]
            longitude = wpt[0]
            elevation = wpt[2]
            trackpoints.append(Trackpoint(latitude=latitude, longitude=longitude, elevation=elevation))
      else:
        name = placemark.findtext('{*}name')
        notes = placemark.findtext('{*}description')
        coords = placemark.find('{*}Point/{*}coordinates').text.strip().split(',')
        latitude = coords[1]
        longitude = coords[0]
        POI_list.append(POI(latitude=latitude, longitude=longitude, name=name, notes=notes))
    return metadata, trackpoints, POI_list

class KMZ(KML):
  pass

class TCX:
  def parse(filepath):
    tree = ET.parse(filepath)
    root = tree.getroot()
    name = root.findtext('.//{*}CourseNameRef/{*}Id')
    metadata = Metadata(name=name)
    trackpoints = []
    for trkpt in root.findall('.//{*}Trackpoint'):
      latitude = trkpt.findtext('{*}Position/{*}LatitudeDegrees')
      longitude = trkpt.findtext('{*}Position/{*}LongitudeDegrees')
      elevation = trkpt.findtext('{*}AltitudeMeters')
      distance = trkpt.findtext('{*}DistanceMeters')
      trackpoints.append(Trackpoint(latitude=latitude, longitude=longitude, elevation=elevation,  distance=distance))
    POI_list = []
    for crspt in root.findall('.//{*}CoursePoint'):
      name = crspt.findtext('{*}Name')
      latitude = crspt.findtext('{*}Position/{*}LatitudeDegrees')
      longitude = crspt.findtext('{*}Position/{*}LongitudeDegrees')
      type_ = crspt.findtext('{*}PointType')
      notes = crspt.findtext('{*}Notes')
      POI_list.append(POI(latitude=latitude, longitude=longitude, name=name, type_=type_, notes=notes))
    return metadata, trackpoints, POI_list

  def build(metadata, trackpoints, POI_list, tolerance=100):
    root = ET.Element('TrainingCenterDatabase')
    folders = ET.SubElement(root, 'Folders')
    folders_courses = ET.SubElement(folders, 'Courses')
    folders_courses_coursefolder = ET.SubElement(folders_courses, 'CourseFolder')
    folders_courses_coursefolder.set('Name', 'Courses')
    folders_courses_coursefolder_coursenameref = ET.SubElement(folders_courses_coursefolder, 'CourseNameRef')
    ET.SubElement(folders_courses_coursefolder_coursenameref, 'Id').text = metadata.name
    courses = ET.SubElement(root, 'Courses')
    course = ET.SubElement(courses, 'Course')
    ET.SubElement(course, 'Name').text = metadata.name
    track = ET.SubElement(course, 'Track')
    if not trackpoints[0].distance:
      distances = []
      for i,trackpoint in enumerate(trackpoints):
        if i == 0:
          distances.append(0)
        else:
          distances.append(distances[-1] + geodesic(trackpoints[i-1].coords, trackpoint.coords).m)
    for i,trackpoint in enumerate(trackpoints):
      trkpt = ET.Element('Trackpoint')
      position = ET.SubElement(trkpt, 'Position')
      ET.SubElement(position, 'LatitudeDegrees').text = trackpoint.latitude
      ET.SubElement(position, 'LongitudeDegrees').text = trackpoint.longitude
      ET.SubElement(trkpt, 'AltitudeMeters').text = trackpoint.elevation
      ET.SubElement(trkpt, 'DistanceMeters').text = trackpoint.distance if trackpoint.distance else str(distances[i])
      track.append(trkpt)
    for i,poi in enumerate(POI_list):
      print(i+1, poi.name, file=sys.stderr)
      coursepoint = ET.Element('CoursePoint')
      ET.SubElement(coursepoint, 'Name').text = poi.name
      ET.SubElement(coursepoint, 'Notes').text = poi.notes
      ET.SubElement(coursepoint, 'PointType').text = poi.type_ if poi.type_ else 'Generic'
      distances = []
      for trackpoint in trackpoints:
        distances.append(geodesic(poi.coords, trackpoint.coords).m)
      min_idx = numpy.argmin(numpy.array(distances))
      if distances[min_idx] < tolerance:
        print("found nearest trackpoint: {:.2f} m".format(distances[min_idx]), file=sys.stderr)
      else:
        print(Color.YELLOW + "skip" + Color.END, file=sys.stderr)
        continue
      position = ET.SubElement(coursepoint, 'Position')
      ET.SubElement(position, 'LatitudeDegrees').text = trackpoints[min_idx].latitude
      ET.SubElement(position, 'LongitudeDegrees').text = trackpoints[min_idx].longitude
      course.append(coursepoint)
    return root

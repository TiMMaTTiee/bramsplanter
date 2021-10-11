from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ShoeModel(Base):
    __tablename__ = 'shoe_models'

    id = Column(Integer, primary_key=True)
    model = Column(String(45))
    size = Column(Integer)
    path_to_cad = Column(String(45))
    margin_a = Column(Integer)
    margin_b = Column(Integer)
    margin_c = Column(Integer)
    margin_d = Column(Integer)


class Scan(Base):
    __tablename__ = 'scans'

    id = Column(Integer, primary_key=True)
    UUID = Column(String(45))
    shoe_id = Column(ForeignKey('shoe_models.id'), index=True)
    scan_type = Column(String(45))
    progress = Column(Integer)
    video_path = Column(String(45))
    error = Column(Integer)
    timestamp_received = Column(DateTime)
    timestamp_processed = Column(DateTime)
    shoe = relationship('ShoeModel')


class Alignment(Base):
    __tablename__ = 'alignment'

    id = Column(Integer, primary_key=True)
    scan_id = Column(ForeignKey('scans.id'), index=True)
    best_size = Column(Integer)
    fit_found = Column(TINYINT(1))
    margin_a = Column(Integer)
    margin_b = Column(Integer)
    margin_c = Column(Integer)
    margin_d = Column(Integer)
    message = Column(String(45))
    complete = Column(TINYINT(1))
    error = Column(Integer)
    scan = relationship('Scan')


class FootSelector(Base):
    __tablename__ = 'foot_selector'

    id = Column(Integer, primary_key=True)
    scan_id = Column(ForeignKey('scans.id'), index=True)
    selected_foot = Column(String(45))
    foot_length = Column(Integer)
    pointcloud_output_path = Column(String(45))
    message = Column(String(45))
    complete = Column(TINYINT(1))
    error = Column(Integer)
    scan = relationship('Scan')


class FrameClipper(Base):
    __tablename__ = 'frame_clipper'

    id = Column(Integer, primary_key=True)
    scan_id = Column(ForeignKey('scans.id'), index=True)
    output_path = Column(String(45))
    message = Column(String(45))
    complete = Column(TINYINT(1))
    error = Column(Integer)
    scan = relationship('Scan')


class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True)
    scan_id = Column(ForeignKey('scans.id'), index=True)
    message = Column(String(45))
    timestamp_received = Column(DateTime)
    timestamp_processed = Column(DateTime)
    scan = relationship('Scan')


class ScaleDetector(Base):
    __tablename__ = 'scale_detector'

    id = Column(Integer, primary_key=True)
    scan_id = Column(ForeignKey('scans.id'), index=True)
    pointcloud_output_path = Column(String(45))
    topview_output_path = Column(String(45))
    detected_scale = Column(String(45))
    message = Column(String(45))
    complete = Column(TINYINT(1))
    error = Column(Integer)
    scan = relationship('Scan')


class ScanMetadatum(Base):
    __tablename__ = 'scan_metadata'

    id = Column(Integer, primary_key=True)
    scan_id = Column(ForeignKey('scans.id'), index=True)
    shoe_model_id = Column(Integer)
    paper_size = Column(String(45))
    requestee = Column(String(45))
    scan = relationship('Scan')


class StructureFromMotion(Base):
    __tablename__ = 'structure_from_motion'

    id = Column(Integer, primary_key=True)
    scan_id = Column(ForeignKey('scans.id'), index=True)
    pointcloud_output_path = Column(String(45))
    mesh_output_path = Column(String(45))
    progress = Column(Integer)
    message = Column(String(45))
    complete = Column(TINYINT(1))
    error = Column(Integer)
    scan = relationship('Scan')


class Phase(Base):
    __tablename__ = 'phases'

    id = Column(Integer, primary_key=True)
    phase = Column(String(45))


class Error(Base):
    __tablename__ = 'errors'

    id = Column(Integer, primary_key=True)
    message = Column(String(45))


class Warning(Base):
    __tablename__ = 'warnings'

    id = Column(Integer, primary_key=True)
    warning = Column(String(45))

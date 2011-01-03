import api
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, Index, DateTime
from sqlalchemy.orm import relationship, backref
import database

class HITGroup(database.Base):
    __tablename__ = "turkic_hit_groups"

    id          = Column(Integer, primary_key = True)
    title       = Column(String(250), nullable = False)
    description = Column(String(250), nullable = False)
    duration    = Column(Integer, nullable = False)
    lifetime    = Column(Integer, nullable = False)
    cost        = Column(Float, nullable = False)
    keywords    = Column(String(250), nullable = False)
    height      = Column(Integer, nullable = False, default = 650)

class Worker(database.Base):
    __tablename__ = "turkic_workers"

    id             = Column(String(14), primary_key = True)
    numsubmitted   = Column(Integer, nullable = False, default = 0)
    numacceptances = Column(Integer, nullable = False, default = 0)
    numrejections  = Column(Integer, nullable = False, default = 0)
    trained        = Column(Boolean, default = False)
    trusted        = Column(Boolean, default = False)
    blocked        = Column(Boolean, default = False)

    def block(self):
        api.server.block(self.id)

    def unblock(self):
        api.server.unblock(self.id)

class HIT(database.Base):
    __tablename__ = "turkic_hits"

    id            = Column(Integer, primary_key = True)
    hitid         = Column(String(30))
    groupid       = Column(Integer, ForeignKey(HITGroup.id), index = True)
    group         = relationship(HITGroup, cascade = "all", backref = "hits")
    assignmentid  = Column(String(30))
    workerid      = Column(Integer, ForeignKey(Worker.id), index = True)
    worker        = relationship(Worker, cascade = "all", backref = "tasks")
    published     = Column(Boolean, default = False, index = True)
    completed     = Column(Boolean, default = False, index = True)
    compensated   = Column(Boolean, default = False, index = True)
    accepted      = Column(Boolean, default = False, index = True)
    reason        = Column(Text)
    comments      = Column(Text)
    timeaccepted  = Column(DateTime)
    timecompleted = Column(DateTime)
    page          = Column(String(250), nullable = False, default = "")

    def publish(self):
        resp = api.server.createhit(
            title = self.group.title,
            description = self.group.description,
            amount = self.group.cost,
            duration = self.group.duration,
            lifetime = self.group.lifetime,
            keywords = self.group.keywords,
            height = self.group.height,
            page = self.page
        )
        self.hitid = resp.hit_id
        self.published = True

    def accept(self, reason = ""):
        api.server.accept(self.assignmentid, reason)
        self.accepted = True
        self.compensated = True

    def reject(self, reason = ""):
        api.server.reject(self.assignmentid, reason)
        self.accepted = False
        self.compensated = True
    
    def awardbonus(self, amount, reason):
        pass

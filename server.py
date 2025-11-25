class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

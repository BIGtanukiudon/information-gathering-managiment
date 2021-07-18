from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database.config import Base


class Account(Base):
    __tablename__ = "account"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)

    collection_destinations = relationship(
        "CollectionDestination", back_populates="account")


class CollectionDestination(Base):
    __tablename__ = "collection_destination"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    domain = Column(String)
    contents_attr_name = Column(String)
    title_attr_name = Column(String)
    published_date_attr_name = Column(String)
    is_getting_domain = Column(Boolean, default=False)
    domain_attr_name = Column(String)
    content_url_attr_name = Column(String)
    account_id = Column(Integer, ForeignKey("account.id"))

    account = relationship("Account", back_populates="collection_destinations")


class CollectionDestinationForGet(CollectionDestination):
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class CollectionDestinationForCreate(CollectionDestination):
    pass

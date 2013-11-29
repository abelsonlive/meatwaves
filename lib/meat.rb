class Meat 
  include DataMapper::Resource

  property :id,         Serial
  property :key,        String
  property :gif,        String
  property :message     String

end

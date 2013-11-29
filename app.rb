require 'bundler'
Bundler.require

class Meat 
  includes DataMapper:Resource

  property :id,         Serial
  property :key,        String, :required => true
  property :gif,        String, :required => true
  property :message     String, :required => true
  property :fingerprint String, :required => true

end


class App < Sinatra::Base

  db = SQLite::Database.new( "meats.db" )

  get "/" do
    "YO BRIAN"
  end

	#get "/meats/" do
	#	@meats = Meat.all
  #  haml :index
	#end

  #get "/meats/:id" do
  #  @meat = Meat.get(:id)
  #  haml :meat
  #end

  post "/meats/new/" do
    @params = params.inspect
    haml :debug
  end

end

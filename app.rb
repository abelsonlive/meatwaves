require 'bundler'
Bundler.require

#Dir.glob('./lib/*.rb') do |model|
#  require model
#end

class App < Sinatra::Base

  set :database, "sqlite3:///meats.db"

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

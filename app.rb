require 'bundler'
Bundler.require

Dir.glob('./lib/*.rb') do |model|
  require model
end

set :database, "sqlite3:///meats.db"

class App < Sinatra::Base

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
    @meat = Meat.new( id: params["id"],
                      key: params["key"],
                      gif: params["gif"],
                      message: params["message"],
                      created: params["created"],
                      fingerprint: params["fingerprint"] )
    haml :debug
  end

end

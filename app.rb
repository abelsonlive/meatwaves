require 'bundler'
Bundler.require

Dir.glob('./lib/*.rb') do |model|
  require model
end

set :database, "postgresql://meat:waves@localhost:5432/meat"
set :environment, :production

class App < Sinatra::Base

  get "/" do
    "YO BRIAN"
  end

	get "/meats/" do
		@meats = Meat.all
    
    haml :index
	end

  get "/meats/:fingerprint/" do
    @meats = Meat.where("fingerprint = ? ", params[:fingerprint])
    
    haml :index
  end

  get "/:hashtag/" do
    @meats = Meat.where("hashtag = ? ", params[:hashtag])
  
    haml :index
  end

  get "/meats/:key.gif" do
    @meat = Meat.find_by :key=> params[:key]
    @gif = @meat.gif

    haml :meat
  end

  post "/meats/new/" do
    Meat.create(  :id => params["id"],
                  :key => params["key"],
                  :gif=> params["gif"],
                  :hashtag=> params["hashtag"],
                  :message=> params["message"],
                  :created=> params["created"],
                  :fingerprint=> params["fingerprint"] )
    #haml :debug #FOR DEBUGGS
  end

  get "/meats/recent/" do
    @meat = Meat.first
    @gif = @meat.gif
    haml :meat
  end

  after do
    ActiveRecord::Base.clear_active_connections!
  end

end

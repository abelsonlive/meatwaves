require 'bundler'
Bundler.require

class App < Sinatra::Base

	set :database, "sqlite3:///database.db"

	get "/" do
		"Hello World!"
	end

end

require 'rubygems'
require 'HTTParty'
require 'nokogiri'
require 'JSON'
require 'pry'
require 'csv'
require 'mechanize'
require 'irbtools'

mech = Mechanize.new
sessions = %w(6575 6604 6635 6670 6845)

def self.strip
  self.gsub(/\A"|"\Z/, '').gsub(/\n/,"").strip
end

CSV.open('results.csv', 'w') do |csv|

  sessions.each do |session|
    url = 'http://behaviour-2015.m.asnevents.com.au/schedule/session/' + session + '?_pjax=%23pjax-container'
    page = mech.get(url)




    array = []
    puts ">>>BEGIN====================================================="
    loop do
      puts "URL: " + page.uri.to_s
      puts "TITLE: " + page.title
      puts "ABSTRACT LINKS: " + page.links_with(:href => /abstract+\/(\d....)/).count.to_s

      abstracts = page.links_with(:href => /abstract+\/(\d....)/)

      if !abstracts.empty?
        abstracts.each_with_index do |abstract, i|
          new_page = mech.click(abstract)
          if new_page.at('#Title') != nil
            puts "Found Abstract "+ (i+1).to_s + ": " + new_page.at('#Title')

            new_row = []
            title = new_page.at('#Title').text.strip
            author = new_page.at('.author.presenting').xpath('span').text.strip
            abstract = new_page.at('#abstractContent').xpath('p').text.strip
            uni = new_page.at('ol.affiliations li').text.strip rescue "-"
            new_row << [author, title, abstract, uni]

            # navigate to new link
            csv << new_row
          end
        end
      end

      puts "<<<END====================================================="
      puts ""
      puts ""

      # Navigate to new nav link
      if link =  page.at("#next-tab a")
        url = link['href'] + '?_pjax=%23pjax-container'
        page = mech.get(url)

        puts ">>> clicking into: " + link['href']
        puts ""
        puts ">>>BEGIN====================================================="
      else
        break #exit program
      end
    end


  end
end





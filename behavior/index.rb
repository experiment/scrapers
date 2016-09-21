require 'rubygems'
require 'HTTParty'
require 'nokogiri'
require 'JSON'
require 'pry'
require 'csv'
require 'mechanize'

sessions = [6573, 6595]
# sessions = [6573, 6574, 6575, 6576, 6606, 6577, 6578, 6587, 6580, 6581, 6611, 6582, 6643, 6584, 6585, 6579, 6588, 6848, 7026, 6592, 6594, 6595, 6596, 6597, 6599, 6590, 7027, 6601, 6602, 6603, 6604, 6605, 6607, 6608, 6627, 6610, 6613, 6615, 6621, 6616, 6617, 6618, 6609, 6620, 6622, 6623, 6629, 6624, 6625, 6626, 6619, 6628, 6630, 6631, 6632, 6633, 6634, 7132, 7197, 6635, 6636, 6638, 6639, 6640, 6642, 6645, 6647, 6648, 6649, 7133, 7161, 7134, 6650, 6651, 6654, 6656, 6657, 6659, 6661, 6669, 6662, 6664, 6665, 6666, 6667, 6668, 7198, 6670, 6671, 6672, 6673, 6675, 6676, 6677, 6678, 6679, 6702, 6681, 6683, 6685, 6686, 7232, 6690, 6680, 6692, 6694, 6697, 6698, 7233, 6701, 6691, 6703, 6707, 6708, 6709, 6710, 6711, 6712, 6845, 6688, 6847, 6855, 6849, 6851, 6852, 6853, 6846, 6854, 6856, 7234, 6857, 6858, 6859, 7199]

sessions.each do |ses|
  url = "http://behaviour-2015.m.asnevents.com.au/schedule/session/#{ses}?_pjax=%23pjax-container"
  puts url

  parse = HTTParty.get(url)
  doc = Nokogiri::HTML(parse)

  mech = Mechanize.new
  mech_page = mech.get(url)


  array = []
  loop do

    if mech_page.at('#Title') == nil # TITLE IS NOT PRESENT
      if next_session_link = (mech_page.link_with(:href => /session/))
        mech_page = mech.click(next_session_link)
      else
        # no link to new session, break to next session index
        break
      end



      new_row = []
      title = mech_page.at('#Title').text.gsub(/\A"|"\Z/, '').gsub(/\n/,"")
      puts mech_page.at('#Title')
      author = mech_page.at('.author.presenting').xpath('span').text.gsub(/\A"|"\Z/, '').gsub(/\n/,"")
      abstract = mech_page.at('#abstractContent').xpath('p').text.gsub(/\A"|"\Z/, '').gsub(/\n/,"")

      new_row << [author, title, abstract]
      array << new_row

      if link =  mech_page.at("#next-tab a") #["href", "/schedule/session/6624/abstract/24456"
        mech_page = mech.click(link)
      else
        break
      end
    else
    end

  end
  CSV.open('results.csv', 'w') do |csv|
    csv
    csv << array
  end
end




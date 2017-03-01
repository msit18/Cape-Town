#This code is written by Michelle Sit

#Notes:
#When putting values into the hash table, you must input the values into the variable "json".
#If you create a variable to hold the json values and input the values into that variable,
#the values will not transfer to the json that is written into the system.

#For Cloudant, you must include the _id and _rev items to write to the online database

#convoNum behaviors - It must never go to 0 otherwise there will be one too many survey items
#- At 1 = lowest number. input +1
#- At 5 = input should +1
#- At 6 = If input, produce new survey set, reset convoNum to 1

#Everything in the json starts from 1 instead of 0. This is to improve readability for
#non-computer science people.

require 'rubygems' 
require 'net/http' 
require 'json' 
 
#This is the HTTP request for CouchDB class 
module Couch 
 
  class Server 
    def initialize(host, port, options = nil) 
      #log "SERVER INITIALIZED AND ESTABLISHING VARIABLES------------------------------------"
      @host = host 
      @port = port 
      @options = options 
    end 

    def request(req) 
      res = Net::HTTP.start(@host, @port) { |http|http.request(req) } 
      unless res.kind_of?(Net::HTTPSuccess) 
        handle_error(req, res) 
      end 
      res 
    end 

    def DELETE(uri) 
      request(Net::HTTP::Delete.new(uri)) 
    end 

    def GET(uri) 
      request(Net::HTTP::Get.new(uri)) 
    end 

    def PUT(uri, json) 
      req = Net::HTTP::Put.new(uri) 
      req["content-type"] = "application/json"
      req.body = json 
      request(req) 
    end 

    def handle_error(req, res) 
      e = RuntimeError.new("#{res.code}:#{res.message}\nMETHOD:#{req.method}\nURI:#{req.path}\n#{res.body}") 
      raise e 
    end
  end 

end

class Citivan
  def initialize (callerID)
    #log "INITIALZIING CITIVAN-----------------------------------------------------------------------"
    @callerID = callerID
    #log "ESTABLISHED CALLERID VARIABLE---------------------------------------------------------------"
    @json = getDBData("http://citivan.cloudant.com/citivan/testSample2/")
    #log "First @JSON: #{@json}"
    #log "ESTABLISHED JSON VALUE----------------------------------------------------------------------"
    @callerHashInfo = @json["people"]["#{callerID}"]
    log "ESTABLISHED CALLERHASHINFO VALUE. END OF INITIALIZED-------------------------------------------------------------"
  end

  #This is a helper method to get data from couchDB 
  def getDBData(urlInput)
    #log "GETDBDATA BEFORE URL-------------------------------------------------------------------------"
    url = URI.parse(urlInput)
    #log "AFTER URL, BEFORE CONNECTING TO SERVER--------------------------------------------------------"
    server = Couch::Server.new(url.host, url.port)
    #log "CONNECTED TO SERVER NOW GETTING URL-----------------------------------------------------------"
    res = server.GET(urlInput)
    log "PARSING JSON FILE----------------------------------------------------------------------------"
    json = JSON.parse(res.body)
    return json
  end

  def getBusName(callerID, userText)
    log "GETBUSNAME RUNNING"
    @busName = @json["people"]["#{callerID}"]["#{@surveyNum}"]["1"]
    log "BUSNAME: #{@busName}"
    if @busName.to_s == "0"
      @busName = userText
      if @busJson.has_key?(userText.to_s) == false && userText != "rate"
        log "CREATING NEW BUS DATA"
        @busJson["#{userText}"] = {"1" => "#{userText}", "2" => 0, "3" => 0, "4" => 0, "5" => 0, "6" => 0, "7" => 0, "8" => 0, "9" => 0, "10" => 0}
      end
      log "MAYBE CREATED NEW SURVEY?"
    end
    return @busName
  end

  def calculateAverage(inputBusName, questionNum)
    return avg = (@busJson["#{inputBusName}"]["#{questionNum}"].to_f)/(@busJson["#{inputBusName}"]["#{questionNum +5}"])*100
  end

  #FIX: needs smart handling for bus numbers that start with rat or rtae
  def rateBus(userText, currentConvoNum)
    log "RATE FUNCTION"
    log userText
    log userText.slice!(0..4)
    log rateBusName = userText
    log @busJson.has_key?(rateBusName)
    log @busJson["#{rateBusName}"]
    if @busJson.has_key?(rateBusName) == false
      log "BUS HAS NOT BEEN RATED YET"
      return overrideReturnValue = "The bus #{rateBusName} has not been rated yet."\
      "@@#{$questions[currentConvoNum-1]}"
    elsif @busJson["#{rateBusName}"]["10"] == 0
      return overrideReturnValue = "The bus #{rateBusName} has not been rated yet."\
      "@@#{$questions[currentConvoNum-1]}"
    else
      log "BUS RATING IS THE FOLLOWING"
      question2Answer = calculateAverage(rateBusName, 2)/100
      return overrideReturnValue = "Rating for #{rateBusName} from #{@busJson[rateBusName]["10"]} riders:\n"\
      "Avg quality of ride: #{question2Answer}/5\n"\
      "#{calculateAverage(rateBusName, 3)}% think the driver speeds.\n"\
      "#{calculateAverage(rateBusName, 4)}% think the driver is courteous.\n"\
      "#{calculateAverage(rateBusName, 5)}% think the van is clean."\
      "@@#{$questions[currentConvoNum-1]}"
    end
  end

  #TODO: Revise when the bus ID format is provided
  def inputDataToCloudant(currentConvoNum, callerID, userText)
    log "INPUTTING DATA FUNCTION"
    log currentConvoNum
    getBusName(callerID, userText)
    log userText
    #All the incorrect inputs
    if currentConvoNum == 1
      log "FIRST QUESTION. PUTTING BUS NAME INTO THE SYSTEM"
      @json["people"]["#{callerID}"]["#{@surveyNum}"]["#{currentConvoNum}"] = userText
      @busJson["#{@busName}"]["#{currentConvoNum +5}"] += 1
      @json["people"]["#{callerID}"]["convoNum"] += 1
    elsif currentConvoNum == 2 && userText.to_i.between?(1,5) == true
      log "QUESTION TWO. PUTTING IN INFO"
      @json["people"]["#{callerID}"]["#{@surveyNum}"]["#{currentConvoNum}"] = userText.to_i
      @busJson["#{@busName}"]["#{currentConvoNum}"] += userText.to_i
      @busJson["#{@busName}"]["#{currentConvoNum +5}"] += 1
      @json["people"]["#{callerID}"]["convoNum"] += 1
    elsif currentConvoNum > 2 && (userText.to_s == "yes" || userText.to_s == "no" || userText.to_i.between?(1,2))
      log "QUESTIONS THREE THROUGH FIVE. PUTTING IN INFO"
      if userText.to_s == "yes" || userText.to_i == 1
        @json["people"]["#{callerID}"]["#{@surveyNum}"]["#{currentConvoNum}"] = "yes"
        @busJson["#{@busName}"]["#{currentConvoNum}"] += 1
      elsif userText.to_s == "no" || userText.to_i == 2
        @json["people"]["#{callerID}"]["#{@surveyNum}"]["#{currentConvoNum}"] = "no"
        #Does not add to busJson question number if the answer is no
      end
      @busJson["#{@busName}"]["#{currentConvoNum +5}"] += 1
      @json["people"]["#{callerID}"]["convoNum"] += 1
    else
      #Repeat question
    end
  end

  ###MAIN METHOD
  def runNew(callerID, userText)
    #Connects to database server in initilize
    begin
    log "RUNNING BEGIN OF RUN NEW----------------------------------------------------------"
      ###DOES USER EXIST? If so, then all the other functions are allowed.
      #If this is a new user, disregard the input text and just create a new profile
      if @json["people"].has_key?(callerID.to_s) == true
        log "VERIFY USER EXISTS: USER ALREADY EXISTS"
        newUser = false
        @busJson = getDBData("http://citivan.cloudant.com/citivan/busData/")

        #Creates new survey hash if last is full
        if @callerHashInfo["convoNum"] > 5 && userText != "rate"
          log "CREATING NEW SURVEY HASH. LAST SURVEY IS FULL"
          @json["people"]["#{callerID}"]["convoNum"] = 1
          @json["people"]["#{callerID}"]["#{@callerHashInfo.length-1}"] = {"1" => 0, "2" => 0, "3" => 0, "4" => 0, "5" => 0}
        else
          currentConvoNum = @callerHashInfo["convoNum"]
          log "NUM ITEMS IN CALLERID: #{@callerHashInfo.length}"
          @surveyNum = @callerHashInfo.length-1 #Note: convoNum item is removed from length
          overrideReturnValue = nil

          ###RATE CMD
          if userText.start_with?("rate ") == true
            overrideReturnValue = rateBus(userText, currentConvoNum)

          ###INPUT TEXT INTO SURVEY
          #TODO: error handling if NIL => repeat question
          else
            log "ELSE STATEMENT"
            inputDataToCloudant(currentConvoNum, callerID, userText)

          end

        end

      ###NEW USER. Create new account. Disregarded input text.
      else
        log "VERIFY USER EXISTS: CREATE NEW PROFILE"
        newCaller = {"1" => {"1" => 0, "2" => 0, "3" => 0, "4" => 0, "5" => 0}, "convoNum" => 1}
        @json["people"]["#{callerID}"] = newCaller
        newUser = true
      
      end #begin if/elseEnd
    
    ensure
      log "overrideReturnValue: #{overrideReturnValue}"
      log overrideReturnValue == nil
      if overrideReturnValue == nil
        ###Note: store information into user databases
        returnValue = @json["people"]["#{callerID}"]["convoNum"]
        jsonFormat = @json.to_json
        url = URI.parse("http://citivan.cloudant.com/citivan/testSample2/") 
        server = Couch::Server.new(url.host, url.port) 
        server.PUT("http://citivan.cloudant.com/citivan/testSample2/", jsonFormat) 
        if newUser == false
          busJsonFormat = @busJson.to_json
          busUrl = URI.parse("http://citivan.cloudant.com/citivan/busData/") 
          busServer = Couch::Server.new(url.host, url.port) 
          busServer.PUT("http://citivan.cloudant.com/citivan/busData/", busJsonFormat)
        end
      else
        returnValue = overrideReturnValue
      end
      log "RETURNVALUE: #{returnValue}"
    return returnValue
    
    end #begin/ensureEnd

  end #defEnd

end #citivanServer End

def simulateSMS2(callerID, initialText)
  reply = initialText.downcase
  connect = Citivan.new(callerID.to_s)
  status = connect.runNew(callerID.to_s, reply)
  log "CELLPHONE TEXT:"
  if status.class != String && status.to_i <= 1
      log "Welcome to CitiVan! Please answer the following questions. To see the ratings of a van, send \"rate VanNumber\""
      #wait(3000)
      log "#{$questions[0]}"
  elsif status.class != Fixnum
      statusSplit = status.split('@@')
      log "#{statusSplit[0]}"
      #wait(2000)
      log "Split here"
      log "#{statusSplit[1]}"
  else
      log "#{$questions[status-1.to_i]}"
  end
  log "END OF CELLPHONE TEXT"
end


############### Main method starts here:


#Text messages to send to user
$questions = ["What is your bus number?", "Pick a number from 1 to 5 to rate the quality of your ride. 1) Very poor. 2) Poor. 3) Average. 4) Good. 5) Excellent.",
"Was your driver speeding? Enter 1 for yes or 2 for no.", "Was your driver courteous? Enter 1 for yes or 2 for no.",
"Was your minibus clean? Enter 1 for yes or 2 for no.", "Thank you for your responses! Have a great day."]

###################Execute code here

#log "Welcome. What is your callerID?"
#caller = gets.chomp!

#continue = true
#while continue == true
#  log "What is your message?"
#  input = gets.chomp!
#  if input == "stop"
#    break
#  else
#    simulateSMS2(8583807847, input)
#  end
#end

#log "Current call is active4 #{$currentCall.isActive}-----------------------------------------------"
if $currentCall.isActive
    log "CURRENT CALL PHONE NUMBER IS #{$currentCall.callerID}---------------------------------------"
    #say "Current active phone is2 #{$currentCall.callerID}"
else
    #call "+17788061682", { :network => "SMS"}
    call "+13392044253", { :network => "SMS"}
    #say "started new call2"
end


log "BEFORE REPLY --------------------------------------------"
reply = $currentCall.initialText.downcase
log "REPLY IS #{reply}"
log "BEFORE CONNECT ------------------------------------------------------------------"
connect = Citivan.new($currentCall.callerID.to_s)
log "AFTER CONNECT --------------------------------------------------------"
status = connect.runNew($currentCall.callerID.to_s, reply)
log "STATUS IS #{status}"
if status.class != String && status.to_i <= 1
    log "WELCOME TO CITIVAN---------------------------------------------------------------------"
    say "Welcome to CitiVan! Please answer the following questions. To see the ratings of a van, send \"rate VanNumber\""
    log "SEND WELCOME MESSAGE--------------------------------------------------------------------"
    wait(3000)
    say "#{$questions[0]}"
    log "SENT #{$questions[0]}--------------------------------------------------------------------"
elsif status.class != Fixnum
    log "STATUS CLASS FIXNUM----------------------------------------------------------------"
    statusSplit = status.split('@@')
    say "#{statusSplit[0]}"
    log "SENT SPLIT STATUS #{statusSplit[0]}----------------------------------------------------------------"
    wait(2000)
    say "#{statusSplit[1]}"
    log "SEND SPLIT STATUS PART 2 #{statusSplit[1]}---------------------------------------------------------"
else
    log "ELSE VALUE RUNNING-----------------------------------------------------------------------"
    say "#{$questions[status-1.to_i]}"
    log "SENT MESSAGE #{$questions[status-1.to_i]}------------------------------------------------------------"
end

hangup
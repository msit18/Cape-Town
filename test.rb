say "running"
log "Current call is active #{$currentCall.isActive}------------------------------------------------"
call "+18572390034", { :network => "SMS"}
log "new message------------------------------------------------------------------------------------"
log "CITIVAN #{Citivan.new($currentCall.callerID.to_s)}---------------------------------------------"
log "Current call is active2 #{$currentCall.isActive}-----------------------------------------------"
connect = Citivan.new($currentCall.callerID.to_s)
log "After conenct-----------------------------------------------------------------------------------"
while True:
    log "WHILE LOOP RUNNING -----------------------------------------------------------------------"
    reply = $currentCall.initialText.downcase
    log "REPLY IS #{reply}"
    status = connect.runNew($currentCall.callerID.to_s, reply)
    log "STATUS IS #{status}"
    if status.class != String && status.to_i <= 1
        say "Welcome to CitiVan! Please answer the following questions. To see the ratings of a van, send \"rate VanNumber\""
        wait(3000)
        say "#{$questions[0]}"
    elsif status.class != Fixnum
        say "#{status}"
    else
        say "#{$questions[status-1.to_i]}"
    end
end
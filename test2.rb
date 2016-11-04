def orState(input)
	if input.start_with?("rate") || input.start_with?("rat") == true
		puts "TRUE"
	else
		puts "FALSE"
	end
end

orState("rate busbus")
orState("rat busbus")

splitStr ="pop pop pop pop## hi hi hi".split('##')
puts splitStr[0]
puts "LDKJFLDS"
puts splitStr[1]

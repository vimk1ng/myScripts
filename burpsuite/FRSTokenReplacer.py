print "Loading FRSTokenReplacer"
print "FRS Token Extractor and Inserter"
print "Remember to update token details in the extension!"

# You need to import the interfaces you want to use here there's a list in the
# API documentation! https://portswigger.net/burp/extender/api/
# In this module, I'm just messing with requests so only need the basics:
from burp import IBurpExtender
from burp import IHttpListener

# Regex are used for capturing the token value from the response
import re

# In the site I originally wrote this plugin for the token was in a JSON message
# in the strange form name='csrft' value='*', you should change the below so that
# it's appropriate for your target application, taking note of if ' or " are used
# and changing 'csrft' to the name of the token used in your application, e.g.
# RequestVerificationToken, antiCSRF, CSRFtoken, etc.
tokenregex = re.compile(r"access_token\":\"(.*?)\"")

 
class BurpExtender(IBurpExtender, IHttpListener):
    # Variable to hold the token found so that it can be inserted in the next request
    discoveredToken = ''

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("FRSTokenReplacer")
        callbacks.registerHttpListener(self)
        print "Extension registered successfully."
        return

    def processHttpMessage(self, toolFlag, messageIsRequest, currentMessage):
        # Operate on all tools other than the proxy
        #if toolFlag != self._callbacks.TOOL_PROXY:
        if messageIsRequest:
            self.processRequest(currentMessage)
        else:
            self.processResponse(currentMessage)

    def processResponse(self, currentMessage):
        response = currentMessage.getResponse()
        parsedResponse = self._helpers.analyzeResponse(response)
        respBody = self._helpers.bytesToString(response[parsedResponse.getBodyOffset():])

        token = tokenregex.search(respBody)
        if token is not None:
            #print "No token found in response."
        #else:
            BurpExtender.discoveredToken = token.group(1)
            print "Found a token."

    def processRequest(self, currentMessage):
        request = currentMessage.getRequest()
        parsedRequest = self._helpers.analyzeRequest(request)
        requestBody = self._helpers.bytesToString(request[parsedRequest.getBodyOffset():])
        newRequestHeaders = list(parsedRequest.getHeaders())
        
        i = 0
        for header in newRequestHeaders:
            hdOffset = header.find(":")
            if hdOffset != -1:
                hdName = header[:hdOffset]
                #print "Header found: {}".format(header)
                if hdName == "Authorization":
                    if BurpExtender.discoveredToken != '':
                        newRequestHeaders[i] = "Authorization: Bearer " + BurpExtender.discoveredToken
                        print "Replaced Token."
            i += 1

        #if BurpExtender.discoveredToken != '':
            # Here we're using the token name as the start point and an ampersand as the end point
            # so your token must be in the request like csrft=xxxxxx& if there's no trailing amp then
            # this won't work!
            #updatedBody = re.sub(r'csrft=.*?&', 'csrft={0}&'.format(BurpExtender.discoveredToken), requestBody)
            #print "Replaced the token."
       # else:
            # No token to replace, so leave the body as it is
            #updatedBody = requestBody
            #print "No token to replace."

        #updatedRequest = self._helpers.buildHttpMessage(parsedRequest.getHeaders(), updatedBody)
        updatedRequest = self._helpers.buildHttpMessage(newRequestHeaders, requestBody)
        currentMessage.setRequest(updatedRequest)
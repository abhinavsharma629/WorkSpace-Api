def getDeviceDetails(user_agent, request):
    if user_agent.is_pc:
        data=str(request.user_agent.browser.family)+" V- "+str(request.user_agent.browser.version_string)

    elif user_agent.is_tablet or user_agent.is_mobile:
        data=str(request.user_agent.device.family)+" V- "+str(request.user_agent.os.version_string)

    elif user_agent.is_bot:
        data="Bot"
    
    else:
        data="Touch Capable Device"

    return data
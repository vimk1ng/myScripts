$SourceIP = [IPAddress]'192.168.1.11' # Local source IP to scan from
$DestinationPfx = '192.168.1.' # Scan target prefix
$DestinationPort = 80 # Port to scan for

foreach ($ip in 1..254) {
	# get an unused local port, used in local IP endpoint creation
	$UsedLocalPorts = ([System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties()).GetActiveTcpListeners() |
							where -FilterScript {$PSitem.AddressFamily -eq 'Internetwork'} |
							Select -ExpandProperty Port
	do {
			$localport = $(Get-Random -Minimum 49152 -Maximum 65535 )
		} until ( $UsedLocalPorts -notcontains $localport)

	# Create the local IP endpoint, this will bind to a specific N/W adapter for making the connection request
	$LocalIPEndPoint = New-Object -TypeName System.Net.IPEndPoint -ArgumentList  $SourceIP,$localport

	# Create the TCP client and specify the local IP endpoint to be used.
	$TCPClient = New-Object -Typename System.Net.Sockets.TcpClient -ArgumentList $LocalIPEndPoint # by default the proto used is TCP to connect.
	# Combine target address prefix and last octet
	$Destination = [IPAddress]($DestinationPfx+$ip)
	# Connect to the Destination on the required port.
	$conn = $TCPClient.BeginConnect($Destination, $DestinationPort, $null, $null)
	# Specify custom timeout (default is too long)
	$status = $conn.AsyncWaitHandle.WaitOne($(New-TimeSpan -Seconds 1))
	# If connected, echo status
	if ($status -and $TCPClient.Connected)
	{
		echo "$Destination`:$DestinationPort - $($TCPClient.Connected)"
		$TCPClient.Client.Disconnect($true)
	} else {
		# Failed to Connect
		# TODO?
	}
	# Free up client
	$TCPClient.Dispose()
}

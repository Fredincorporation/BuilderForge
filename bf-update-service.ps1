$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = Join-Path $env:USERPROFILE '.local\bin\onchainos.exe'
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.Arguments = 'agent update --agent-id 9604 --service "[{""operation"":""create"",""serviceName"":""Idea-to-Launch Pipeline"",""serviceDescription"":""End-to-end idea-to-launch service: market research, tokenomics, launch assets, smart-contract deployment planning, and on-chain execution support.\nUser provides the idea, target chain, and execution context.\nDelivers a market opportunity report, tokenomics model, deployment plan, and on-chain simulation & verification."",""serviceType"":""A2A"",""fee"":""0.05""}]"'
$p = [System.Diagnostics.Process]::Start($psi)
$out = $p.StandardOutput.ReadToEnd()
$err = $p.StandardError.ReadToEnd()
$p.WaitForExit()
$out
$err
"EXIT=$($p.ExitCode)"

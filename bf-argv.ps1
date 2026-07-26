$psi = [System.Diagnostics.ProcessStartInfo]::new()
$psi.FileName = Join-Path $env:USERPROFILE '.local\bin\onchainos.exe'
$psi.UseShellExecute = $false
$psi.RedirectStandardOutput = $true
$psi.RedirectStandardError = $true
$psi.Arguments = 'agent create --role asp --name BuilderForge --description "An autonomous multi-agent launchpad that converts Web3 ideas into market research, tokenomics, Solidity smart contracts, and OKX X Layer deployments." --picture "https://static.okx.com/cdn/web3/wallet/marketplace/headimages/agent/avatar/7af6186c-12ab-455a-ab0e-295faedf5a93.png" --service "[{""serviceName"":""BuilderForge Launchpad"",""serviceDescription"":""Provides automated Web3 project launch support for AI agents\nYou provide a project proposal and any required inputs\nDelivers market research, tokenomics, Solidity contracts, deployment simulation, and launch-readiness scoring"",""serviceType"":""A2A"",""fee"":""1""}]"'
$p = [System.Diagnostics.Process]::Start($psi)
$out = $p.StandardOutput.ReadToEnd()
$err = $p.StandardError.ReadToEnd()
$p.WaitForExit()
$out
$err
"EXIT=$($p.ExitCode)"

Write-Host "`n=== Testing POST /api/generate ===" -ForegroundColor Cyan
Write-Host "Sending request to generate animation for Pythagoras theorem...`n" -ForegroundColor Yellow

$body = @{
    text = "Animate the Pythagoras theorem with a growing square."
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:3000/api/generate" -Method POST -Body $body -ContentType "application/json"
    
    Write-Host "✅ SUCCESS!" -ForegroundColor Green
    Write-Host "`nResponse:" -ForegroundColor Cyan
    $response | ConvertTo-Json -Depth 10
    
    Write-Host "`n=== Key Information ===" -ForegroundColor Cyan
    Write-Host "Animation ID: $($response.data.id)" -ForegroundColor Yellow
    Write-Host "Status: $($response.data.status)" -ForegroundColor Yellow
    Write-Host "Topic: $($response.data.concept.topic)" -ForegroundColor Yellow
    Write-Host "Objects: $($response.data.concept.objects -join ', ')" -ForegroundColor Yellow
    Write-Host "Number of Scenes: $($response.data.scenes.Count)" -ForegroundColor Yellow
    Write-Host "Timeline Instructions: $($response.data.timeline.Count)" -ForegroundColor Yellow
    
} catch {
    Write-Host "❌ ERROR!" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "`nError Details:" -ForegroundColor Yellow
        $_.ErrorDetails.Message | ConvertFrom-Json | ConvertTo-Json -Depth 5
    }
}

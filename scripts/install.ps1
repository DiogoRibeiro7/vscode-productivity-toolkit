<#
MIT License
Copyright (c) 2025 Diogo Ribeiro

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
#>

[CmdletBinding()]
param(
    [switch] $DryRun,
    [switch] $Silent,
    [string[]] $Categories,
    [string] $SourceRoot,
    [string] $RemoteBaseUrl,
    [switch] $VerboseLogging,
    [switch] $SkipExtensions
)

$ErrorActionPreference = 'Stop'

function Write-Log {
    param(
        [Parameter(Mandatory = $true)][ValidateSet('DEBUG','INFO','WARN','ERROR')] [string] $Level,
        [Parameter(Mandatory = $true)][string] $Message
    )

    if ($Level -eq 'DEBUG' -and -not $VerboseLogging) {
        return
    }

    $payload = [ordered]@{
        timestamp = (Get-Date).ToString('o')
        level = $Level
        message = $Message
    }

    if ($Level -eq 'ERROR') {
        Write-Error -Message ($payload | ConvertTo-Json -Compress)
    }
    else {
        Write-Output ($payload | ConvertTo-Json -Compress)
    }
}

function Register-RollbackAction {
    param(
        [Parameter(Mandatory = $true)] [System.Collections.ArrayList] $Collection,
        [Parameter(Mandatory = $true)] [scriptblock] $Action,
        [object[]] $Arguments
    )

    [void] $Collection.Add([pscustomobject]@{ Action = $Action; Arguments = $Arguments })
}

function Resolve-CodeBinary {
    if ($env:TOOLKIT_CODE_PATH) {
        return $env:TOOLKIT_CODE_PATH
    }

    $command = Get-Command code -ErrorAction SilentlyContinue
    if ($null -ne $command) {
        return $command.Source
    }

    throw 'VS Code command line interface not found. Enable the `code` command and retry.'
}

function Get-CategoryMap {
    $scriptDirectory = Split-Path -Path $MyInvocation.MyCommand.Path -Parent
    $defaultRoot = (Resolve-Path -Path (Join-Path -Path $scriptDirectory -ChildPath '..')).Path
    $resolvedRoot = if ($SourceRoot) { (Resolve-Path -Path $SourceRoot).Path } else { $defaultRoot }

    return @(
        [pscustomobject]@{ Key = 'python-general'; Label = 'Python – General'; Description = 'Quality, packaging, docker, and git automation.'; Path = 'tasks/python/general.json'; Root = $resolvedRoot },
        [pscustomobject]@{ Key = 'python-data-science'; Label = 'Python – Data Science'; Description = 'Notebook conversion, profiling, Sphinx documentation.'; Path = 'tasks/python/data-science.json'; Root = $resolvedRoot },
        [pscustomobject]@{ Key = 'javascript-general'; Label = 'JavaScript/TypeScript – General'; Description = 'Linting, dependency hygiene, documentation.'; Path = 'tasks/javascript/general.json'; Root = $resolvedRoot },
        [pscustomobject]@{ Key = 'javascript-node'; Label = 'Node.js Services'; Description = 'Express workflows, migrations, API testing, publishing.'; Path = 'tasks/javascript/node.json'; Root = $resolvedRoot },
        [pscustomobject]@{ Key = 'javascript-react'; Label = 'React Applications'; Description = 'Component scaffolding, Storybook, bundle analysis, PWA audits.'; Path = 'tasks/javascript/react.json'; Root = $resolvedRoot }
    )
}

function Select-Categories {
    param(
        [Parameter(Mandatory = $true)][System.Collections.IEnumerable] $CategoryMap
    )

    $keys = $CategoryMap | ForEach-Object { $_.Key }
    if ($Categories) {
        $normalized = $Categories | ForEach-Object { $_.ToLowerInvariant() }
        $invalid = $normalized | Where-Object { $keys -notcontains $_ }
        if ($invalid) {
            throw "Unknown categories supplied: $($invalid -join ', ')"
        }
        return $CategoryMap | Where-Object { $normalized -contains $_.Key }
    }

    if ($Silent) {
        return $CategoryMap
    }

    Write-Host ''
    Write-Host 'VS Code Productivity Toolkit Installer' -ForegroundColor Cyan
    Write-Host 'Select the task categories to install:' -ForegroundColor Gray
    $index = 1
    foreach ($category in $CategoryMap) {
        Write-Host ("[{0}] {1} - {2}" -f $index, $category.Label, $category.Description)
        $index++
    }
    Write-Host '[A] All categories'
    Write-Host ''

    while ($true) {
        $selection = Read-Host 'Enter a comma-separated list (e.g. 1,3) or A for all'
        if ([string]::IsNullOrWhiteSpace($selection)) {
            continue
        }

        if ($selection.Trim().ToUpperInvariant() -eq 'A') {
            return $CategoryMap
        }

        $indices = $selection.Split(',') | ForEach-Object { $_.Trim() } | Where-Object { $_ }
        $parsed = @()
        $valid = $true
        foreach ($value in $indices) {
            $parsedValue = 0
            if (-not [int]::TryParse($value, [ref] $parsedValue)) {
                Write-Log -Level 'WARN' -Message "Unable to parse selection '$value'."
                $valid = $false
                break
            }
            $position = [int]$parsedValue
            if ($position -lt 1 -or $position -gt $CategoryMap.Count) {
                Write-Log -Level 'WARN' -Message "Selection '$value' is out of range."
                $valid = $false
                break
            }
            $parsed += $CategoryMap[$position - 1]
        }

        if ($valid -and $parsed.Count -gt 0) {
            return $parsed | Sort-Object -Property Key -Unique
        }

        Write-Host 'Please enter a valid selection.' -ForegroundColor Yellow
    }
}

function Get-TaskContent {
    param(
        [Parameter(Mandatory = $true)][pscustomobject] $Category
    )

    if ($RemoteBaseUrl) {
        $uri = [System.Uri]::new((Join-Path -Path $RemoteBaseUrl.TrimEnd('/') -ChildPath $Category.Path.Replace("\\", '/')))
        Write-Log -Level 'INFO' -Message "Downloading task definition from $($uri.AbsoluteUri)."
        $response = Invoke-WebRequest -Uri $uri -UseBasicParsing -TimeoutSec 60
        return $response.Content
    }

    $filePath = Join-Path -Path $Category.Root -ChildPath $Category.Path
    if (-not (Test-Path -Path $filePath)) {
        throw "Task definition not found: $filePath"
    }
    Write-Log -Level 'DEBUG' -Message "Loading task definition from $filePath."
    return Get-Content -Path $filePath -Raw
}

function ConvertTo-Hashtable {
    param($Object)

    if ($null -eq $Object) { return $null }

    if ($Object -is [System.Collections.IDictionary]) {
        $table = @{}
        foreach ($key in $Object.Keys) {
            $table[$key] = ConvertTo-Hashtable -Object $Object[$key]
        }
        return $table
    }

    if ($Object -is [System.Collections.IEnumerable] -and -not ($Object -is [string])) {
        $items = @()
        foreach ($entry in $Object) {
            $items += ,(ConvertTo-Hashtable -Object $entry)
        }
        return $items
    }

    return $Object
}

function New-TaskAggregate {
    $aggregate = [ordered]@{
        version = '2.0.0'
        schema = 'https://raw.githubusercontent.com/microsoft/vscode/master/src/vs/workbench/contrib/tasks/common/tasks.schema.json'
        inputs = New-Object System.Collections.ArrayList
        tasks = New-Object System.Collections.ArrayList
        problemMatchers = New-Object System.Collections.ArrayList
        metadata = New-Object System.Collections.ArrayList
    }
    return $aggregate
}

function Add-UniqueItem {
    param(
        [Parameter(Mandatory = $true)] [System.Collections.IList] $Collection,
        [Parameter(Mandatory = $true)] $Item,
        [string] $KeyProperty
    )

    if ($null -eq $Item) { return }
    if (-not $KeyProperty) {
        [void] $Collection.Add($Item)
        return
    }

    $value = $Item.$KeyProperty
    if (-not $value) {
        [void] $Collection.Add($Item)
        return
    }

    foreach ($existing in $Collection) {
        if ($existing.$KeyProperty -eq $value) {
            return
        }
    }

    [void] $Collection.Add($Item)
}

function Merge-TaskConfig {
    param(
        [Parameter(Mandatory = $true)] $Aggregate,
        [Parameter(Mandatory = $true)] $Config
    )

    if ($Config.version) {
        $Aggregate.version = $Config.version
    }

    if ($Config.'$schema') {
        $Aggregate.schema = $Config.'$schema'
    }

    if ($Config.inputs) {
        foreach ($input in $Config.inputs) {
            Add-UniqueItem -Collection $Aggregate.inputs -Item $input -KeyProperty 'id'
        }
    }

    if ($Config.tasks) {
        foreach ($task in $Config.tasks) {
            Add-UniqueItem -Collection $Aggregate.tasks -Item $task -KeyProperty 'label'
        }
    }

    if ($Config.problemMatchers) {
        foreach ($matcher in $Config.problemMatchers) {
            Add-UniqueItem -Collection $Aggregate.problemMatchers -Item $matcher -KeyProperty 'name'
        }
    }

    if ($Config._metadata) {
        Add-UniqueItem -Collection $Aggregate.metadata -Item $Config._metadata
    }
}

function Build-TasksConfiguration {
    param(
        [Parameter(Mandatory = $true)] [System.Collections.IEnumerable] $TaskJsonBlocks,
        [string] $ExistingContent
    )

    $aggregate = New-TaskAggregate

    if ($ExistingContent) {
        try {
            $existingConfig = ConvertTo-Hashtable -Object (ConvertFrom-Json -InputObject $ExistingContent -Depth 100)
            Merge-TaskConfig -Aggregate $aggregate -Config $existingConfig
        }
        catch {
            Write-Log -Level 'WARN' -Message 'Existing tasks.json could not be parsed and will be backed up unchanged.'
        }
    }

    foreach ($block in $TaskJsonBlocks) {
        $parsed = ConvertTo-Hashtable -Object (ConvertFrom-Json -InputObject $block -Depth 100)
        Merge-TaskConfig -Aggregate $aggregate -Config $parsed
    }

    $result = [ordered]@{
        '$schema' = $aggregate.schema
        version = $aggregate.version
    }

    if ($aggregate.inputs.Count -gt 0) { $result.inputs = $aggregate.inputs }
    if ($aggregate.tasks.Count -gt 0) { $result.tasks = $aggregate.tasks }
    if ($aggregate.problemMatchers.Count -gt 0) { $result.problemMatchers = $aggregate.problemMatchers }
    if ($aggregate.metadata.Count -gt 0) { $result._toolkitMetadata = $aggregate.metadata }

    return $result | ConvertTo-Json -Depth 100
}

function Install-Extensions {
    param(
        [string] $ExtensionsFile,
        [string] $CodeBinary
    )

    if ($SkipExtensions) {
        Write-Log -Level 'INFO' -Message 'Skipping extension installation as requested.'
        return
    }

    if (-not (Test-Path -Path $ExtensionsFile)) {
        Write-Log -Level 'WARN' -Message "Extensions configuration not found at $ExtensionsFile"
        return
    }

    $extensions = (Get-Content -Path $ExtensionsFile | ConvertFrom-Json).recommendations
    foreach ($extension in $extensions) {
        if (-not $extension) { continue }
        try {
            if (-not $DryRun) {
                & $CodeBinary --install-extension $extension --force | Out-Null
            }
            Write-Log -Level 'INFO' -Message "Ensured extension $extension is installed."
        }
        catch {
            Write-Log -Level 'WARN' -Message "Failed to install extension $extension: $($_.Exception.Message)"
        }
    }
}

try {
    Write-Log -Level 'INFO' -Message 'Starting VS Code productivity toolkit installation.'
    $codeBinary = Resolve-CodeBinary
    Write-Log -Level 'DEBUG' -Message "VS Code CLI resolved to $codeBinary"

    $categoryMap = Get-CategoryMap
    $selectedCategories = Select-Categories -CategoryMap $categoryMap
    if (-not $selectedCategories -or $selectedCategories.Count -eq 0) {
        throw 'No categories selected; installation aborted.'
    }

    $vscodeDir = Join-Path -Path $env:USERPROFILE -ChildPath '.vscode'
    if (-not (Test-Path -Path $vscodeDir)) {
        Write-Log -Level 'INFO' -Message "Creating $vscodeDir directory."
        if (-not $DryRun) { New-Item -ItemType Directory -Path $vscodeDir | Out-Null }
    }

    $tasksFile = Join-Path -Path $vscodeDir -ChildPath 'tasks.json'
    $rollbackActions = [System.Collections.ArrayList]::new()

    if (Test-Path -Path $tasksFile) {
        $backupName = "tasks.json.bak.{0}" -f ([DateTimeOffset]::Now.ToUnixTimeSeconds())
        $backupPath = Join-Path -Path $vscodeDir -ChildPath $backupName
        if (-not $DryRun) {
            Copy-Item -Path $tasksFile -Destination $backupPath -Force
        }
        Register-RollbackAction -Collection $rollbackActions -Action ({ param($source, $target) if (Test-Path -Path $source) { Copy-Item -Path $source -Destination $target -Force } } ) -Arguments @($backupPath, $tasksFile)
        Write-Log -Level 'INFO' -Message "Existing tasks.json backed up to $backupPath."
        $existingContent = Get-Content -Path $tasksFile -Raw
    }
    else {
        $existingContent = $null
    }

    $taskBlocks = @()
    foreach ($category in $selectedCategories) {
        $taskBlocks += ,(Get-TaskContent -Category $category)
    }

    $mergedJson = Build-TasksConfiguration -TaskJsonBlocks $taskBlocks -ExistingContent $existingContent

    if (-not $DryRun) {
        Set-Content -Path $tasksFile -Value $mergedJson -Encoding UTF8
    }
    Write-Log -Level 'INFO' -Message "tasks.json updated with selected categories."

    $settingsDir = Join-Path -Path (Resolve-Path -Path (Join-Path -Path (Split-Path -Path $MyInvocation.MyCommand.Path -Parent) -ChildPath '..')) -ChildPath 'settings'
    foreach ($fileName in @('settings.json','keybindings.json','extensions.json')) {
        $sourceFile = Join-Path -Path $settingsDir -ChildPath $fileName
        if (-not (Test-Path -Path $sourceFile)) { continue }
        $destination = Join-Path -Path $vscodeDir -ChildPath $fileName
        if (Test-Path -Path $destination) {
            $backup = "$fileName.bak.{0}" -f ([DateTimeOffset]::Now.ToUnixTimeSeconds())
            $backupPath = Join-Path -Path $vscodeDir -ChildPath $backup
            if (-not $DryRun) { Copy-Item -Path $destination -Destination $backupPath -Force }
            Register-RollbackAction -Collection $rollbackActions -Action ({ param($source, $target) if (Test-Path -Path $source) { Copy-Item -Path $source -Destination $target -Force } }) -Arguments @($backupPath, $destination)
            Write-Log -Level 'DEBUG' -Message "Backed up $fileName to $backupPath."
        }
        if (-not $DryRun) { Copy-Item -Path $sourceFile -Destination $destination -Force }
        Write-Log -Level 'INFO' -Message "$fileName synchronized to $destination."
    }

    Install-Extensions -ExtensionsFile (Join-Path -Path $settingsDir -ChildPath 'extensions.json') -CodeBinary $codeBinary

    if (-not $DryRun) {
        try {
            $validation = Get-Content -Path $tasksFile -Raw | ConvertFrom-Json -Depth 5
            if (-not $validation.tasks) {
                Write-Log -Level 'WARN' -Message 'No tasks detected in the final tasks.json. Verify your selection.'
            }
        }
        catch {
            throw "tasks.json validation failed: $($_.Exception.Message)"
        }
    }

    Write-Log -Level 'INFO' -Message 'VS Code productivity toolkit installation complete.'
}
catch {
    Write-Log -Level 'ERROR' -Message $_.Exception.Message
    foreach ($rollback in [System.Linq.Enumerable]::Reverse($rollbackActions)) {
        try {
            if (-not $DryRun) {
                & $rollback.Action.Invoke($rollback.Arguments[0], $rollback.Arguments[1]) | Out-Null
            }
        }
        catch {
            Write-Log -Level 'WARN' -Message "Rollback action failed: $($_.Exception.Message)"
        }
    }
    throw
}

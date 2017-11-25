require 'rake'

MODULES = ['lexrank']

TESTS = 'tests'

ROOT_MODULES = ['setup.py']

task default: [:env]

desc 'Display ENV information'
task :env do
  sh 'env'
end

namespace :setup do
  desc 'Install base Python dependencies'
  task :install_base do
    sh 'pip install -U setuptools'
    sh 'pip install -U pip'
    sh 'pip install -U wheel'
    sh 'pip install -U Cython'
    sh 'pip install -r requirements/core.txt'
  end

  desc 'Install Python dependencies for CI'
  task :install_ci do
    Rake::Task['setup:install_base'].invoke
    sh 'pip install -r requirements/ci.txt'
    sh 'pip install .'
  end

  desc 'Install Python dependencies for dev'
  task :install_dev do
    Rake::Task['setup:install_base'].invoke
    sh 'pip install -r requirements/dev.txt'
    sh 'pip install -e .'
  end
end

namespace :dev do
  desc 'Run tests'
  task :test do
    cmd = 'pytest %{tests}'
    cmd = cmd % {tests: TESTS}

    sh cmd
  end

  desc 'Lint code'
  task :lint do
    for package in MODULES + [TESTS]
      cmd = 'flake8 --show-source %{package}'
      cmd = cmd % {package: package}

      sh cmd
    end
    for package in MODULES + [TESTS]
      cmd = 'isort --check-only -rc %{package} --diff'
      cmd = cmd % {package: package}

      sh cmd
    end
    for file in ROOT_MODULES
      for cmd in ['isort --check-only %{file} --diff', 'flake8  --show-source %{file}']
        cmd = cmd % {file: file}

        sh cmd
      end
    end
  end

  desc 'Clean environment'
  task :clean do
    for package in MODULES
      Dir.chdir(package) do
        sh 'find . -type d -name "__pycache__" -exec rm -rf {} + > /dev/null 2>&1'
        sh 'find . -type f -name "*.pyc" -exec rm -rf {} + > /dev/null 2>&1'
      end
    end
  end

end

import re
import os

class ShellScriptComplexityAnalyzer:
    def __init__(self, script_path):
        self.script_path = script_path
        self.complexity_score = 0
        
    def analyze_complexity(self):
        """
        Main method to calculate script complexity
        Returns complexity level: Low, Medium, or High
        """
        try:
            with open(self.script_path, 'r') as file:
                script_content = file.read()
            
            # Reset complexity score
            self.complexity_score = 0
            
            # Run all complexity assessment methods
            self._assess_control_structures(script_content)
            self._assess_external_commands(script_content)
            self._assess_data_transformations(script_content)
            self._assess_error_handling(script_content)
            self._assess_configuration_complexity(script_content)
            
            return self._classify_complexity()
        
        except Exception as e:
            print(f"Error analyzing script {self.script_path}: {e}")
            return "Unable to assess"
    
    def _assess_control_structures(self, content):
        """
        Assess complexity based on control structures
        """
        # Complexity points for different control structures
        control_structures = [
            (r'\bif\b.*\bthen\b', 2),    # Simple if statements
            (r'\bcase\b', 3),            # Case statements
            (r'\bfor\b.*\bin\b', 2),     # For loops
            (r'\bwhile\b', 2),           # While loops
            (r'\buntil\b', 2),           # Until loops
            (r'\belif\b', 3)             # Nested if-else conditions
        ]
        
        for pattern, points in control_structures:
            matches = re.findall(pattern, content, re.MULTILINE)
            self.complexity_score += len(matches) * points
    
    def _assess_external_commands(self, content):
        """
        Assess complexity based on external command usage
        """
        external_command_patterns = [
            r'\bspark-submit\b',         # Spark job submission
            r'\bhadoop\b',               # Hadoop commands
            r'\bhive\b',                 # Hive commands
            r'\baws\b',                  # Cloud service commands
            r'\bscp\b',                  # Secure copy
            r'\brsync\b',                # Remote sync
            r'\bcurl\b',                 # Network requests
            r'\bwget\b'                  # Web download
        ]
        
        for pattern in external_command_patterns:
            matches = re.findall(pattern, content)
            self.complexity_score += len(matches) * 3
    
    def _assess_data_transformations(self, content):
        """
        Assess complexity of data transformation operations
        """
        transform_patterns = [
            r'\bawk\b',                  # Text processing
            r'\bsed\b',                  # Stream editing
            r'\bgrep\b',                 # Text searching
            r'\bcut\b',                  # Column extraction
            r'\bjq\b',                   # JSON processing
            r'\bxmlstarlet\b'            # XML processing
        ]
        
        for pattern in transform_patterns:
            matches = re.findall(pattern, content)
            self.complexity_score += len(matches) * 4
    
    def _assess_error_handling(self, content):
        """
        Assess error handling complexity
        """
        error_handling_patterns = [
            r'\bset\s+-e\b',             # Exit on error
            r'\btrap\b',                 # Signal handling
            r'\bif\s+\[\[.*\]\]\s*;\s*then.*fi',  # Complex error checks
            r'\bif\s+\(\($'               # Advanced error conditions
        ]
        
        for pattern in error_handling_patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            self.complexity_score += len(matches) * 3
    
    def _assess_configuration_complexity(self, content):
        """
        Assess configuration and environment complexity
        """
        config_patterns = [
            r'\bexport\b',               # Environment variables
            r'\bsource\b',               # Sourcing other scripts
            r'\bconfig\b',               # Configuration keywords
            r'\bini\b',                  # Configuration file processing
            r'\bconfig\.'                # Dot-separated config
        ]
        
        for pattern in config_patterns:
            matches = re.findall(pattern, content)
            self.complexity_score += len(matches) * 2
    
    def _classify_complexity(self):
        """
        Classify script complexity based on score
        """
        if self.complexity_score <= 10:
            return "Low"
        elif 10 < self.complexity_score <= 25:
            return "Medium"
        else:
            return "High"

def batch_analyze_scripts(directory):
    """
    Analyze complexity of multiple scripts in a directory
    """
    complexity_summary = {
        "Low": 0,
        "Medium": 0,
        "High": 0
    }
    
    for filename in os.listdir(directory):
        if filename.endswith(('.sh', '.bash')):
            full_path = os.path.join(directory, filename)
            analyzer = ShellScriptComplexityAnalyzer(full_path)
            complexity = analyzer.analyze_complexity()
            complexity_summary[complexity] += 1
            print(f"{filename}: {complexity} Complexity")
    
    return complexity_summary

# Example usage
# complexity = ShellScriptComplexityAnalyzer('/path/to/script.sh').analyze_complexity()
# batch_results = batch_analyze_scripts('/path/to/scripts/directory')

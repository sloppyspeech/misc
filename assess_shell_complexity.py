import re
import os
import glob

class ShellScriptComplexityAnalyzer:
    def __init__(self, script_path):
        self.script_path = script_path
        self.complexity_score = 0
        self.total_lines = 0
        self.meaningful_lines = 0
        self.ecosystem_commands = []
        
    def analyze_complexity(self):
        """
        Main method to calculate script complexity
        Returns complexity level: Low, Medium, or High
        """
        try:
            with open(self.script_path, 'r') as file:
                script_lines = file.readlines()
            
            # Reset complexity score
            self.complexity_score = 0
            self.total_lines = len(script_lines)
            self.ecosystem_commands = []
            
            # Clean and count meaningful lines
            cleaned_lines = self._clean_lines(script_lines)
            self.meaningful_lines = len(cleaned_lines)
            
            # Add line count to complexity score
            self._assess_line_count_complexity()
            
            # Run all complexity assessment methods
            script_content = ''.join(script_lines)
            self._assess_control_structures(script_content)
            self._assess_external_commands(script_content)
            self._assess_data_transformations(script_content)
            self._assess_error_handling(script_content)
            self._assess_configuration_complexity(script_content)
            
            return self._classify_complexity()
        
        except Exception as e:
            print(f"Error analyzing script {self.script_path}: {e}")
            return "Unable to assess"
    
    def _clean_lines(self, lines):
        """
        Remove comments, empty lines, and whitespace-only lines
        """
        def is_meaningful_line(line):
            # Remove leading/trailing whitespace
            stripped = line.strip()
            
            # Ignore empty lines
            if not stripped:
                return False
            
            # Ignore full-line comments
            if stripped.startswith('#'):
                return False
            
            # Remove inline comments
            cleaned = re.sub(r'\s*#.*$', '', stripped)
            
            return bool(cleaned)
        
        return [line for line in lines if is_meaningful_line(line)]
    
    def _assess_line_count_complexity(self):
        """
        Add complexity score based on number of meaningful lines
        """
        # Complexity points based on line count
        if self.meaningful_lines <= 20:
            self.complexity_score += 1
        elif 20 < self.meaningful_lines <= 50:
            self.complexity_score += 3
        elif 50 < self.meaningful_lines <= 100:
            self.complexity_score += 5
        elif 100 < self.meaningful_lines <= 200:
            self.complexity_score += 8
        else:
            self.complexity_score += 12
    
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
        # Ecosystem-specific command patterns
        ecosystem_command_patterns = [
            r'\bhadoop\b',               # Hadoop commands
            r'\bhdfs\b',                 # HDFS commands
            r'\bhive\b',                 # Hive commands
            r'\bspark-submit\b',         # Spark job submission
            r'\bMapReduce\b',            # MapReduce related
            r'\byarn\b'                  # YARN commands
        ]
        
        self.ecosystem_commands = []
        for pattern in ecosystem_command_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                self.ecosystem_commands.extend(matches)
                self.complexity_score += len(matches) * 3
        
        return self.ecosystem_commands
    
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
        # Detailed complexity classification
        complexity_details = {
            "Total Lines": self.total_lines,
            "Meaningful Lines": self.meaningful_lines,
            "Complexity Score": self.complexity_score,
            "Ecosystem Commands": self.ecosystem_commands
        }
        
        if self.complexity_score <= 10:
            return {
                "Level": "Low",
                "Details": complexity_details
            }
        elif 10 < self.complexity_score <= 25:
            return {
                "Level": "Medium", 
                "Details": complexity_details
            }
        else:
            return {
                "Level": "High",
                "Details": complexity_details
            }

def find_shell_scripts(directory):
    """
    Find all shell and bash scripts in a directory and its subdirectories using glob
    """
    # Use double asterisk (**) for recursive matching
    shell_script_patterns = [
        os.path.join(directory, '**', '*.sh'),
        os.path.join(directory, '**', '*.bash')
    ]
    
    # Collect all matching files
    shell_scripts = []
    for pattern in shell_script_patterns:
        shell_scripts.extend(glob.glob(pattern, recursive=True))
    
    return shell_scripts

def batch_analyze_scripts(directory):
    """
    Analyze complexity of multiple scripts in a directory and its subdirectories
    """
    complexity_summary = {
        "Low": 0,
        "Medium": 0,
        "High": 0,
        "Total Scripts": 0,
        "Line Count Statistics": {
            "Min Lines": float('inf'),
            "Max Lines": 0,
            "Average Lines": 0
        },
        "Ecosystem Command Statistics": {
            "Hadoop": 0,
            "HDFS": 0,
            "Hive": 0,
            "Spark": 0,
            "MapReduce": 0,
            "YARN": 0
        }
    }
    
    all_line_counts = []
    
    # Find all shell scripts recursively using glob
    shell_script_paths = find_shell_scripts(directory)
    
    for full_path in shell_script_paths:
        analyzer = ShellScriptComplexityAnalyzer(full_path)
        complexity_result = analyzer.analyze_complexity()
        
        # Update counts
        complexity_summary[complexity_result['Level']] += 1
        complexity_summary['Total Scripts'] += 1
        
        # Track line counts
        line_count = complexity_result['Details']['Total Lines']
        all_line_counts.append(line_count)
        
        # Update min/max line counts
        complexity_summary['Line Count Statistics']['Min Lines'] = min(
            complexity_summary['Line Count Statistics']['Min Lines'], 
            line_count
        )
        complexity_summary['Line Count Statistics']['Max Lines'] = max(
            complexity_summary['Line Count Statistics']['Max Lines'], 
            line_count
        )
        
        # Track ecosystem commands
        ecosystem_commands = complexity_result['Details']['Ecosystem Commands']
        for cmd in ecosystem_commands:
            cmd_lower = cmd.lower()
            if 'hadoop' in cmd_lower:
                complexity_summary['Ecosystem Command Statistics']['Hadoop'] += 1
            if 'hdfs' in cmd_lower:
                complexity_summary['Ecosystem Command Statistics']['HDFS'] += 1
            if 'hive' in cmd_lower:
                complexity_summary['Ecosystem Command Statistics']['Hive'] += 1
            if 'spark' in cmd_lower:
                complexity_summary['Ecosystem Command Statistics']['Spark'] += 1
            if 'mapreduce' in cmd_lower:
                complexity_summary['Ecosystem Command Statistics']['MapReduce'] += 1
            if 'yarn' in cmd_lower:
                complexity_summary['Ecosystem Command Statistics']['YARN'] += 1
        
        # Print detailed information
        print(f"{full_path}: {complexity_result['Level']} Complexity")
        print(f"  Total Lines: {line_count}")
        print(f"  Meaningful Lines: {complexity_result['Details']['Meaningful Lines']}")
        print(f"  Complexity Score: {complexity_result['Details']['Complexity Score']}")
        print(f"  Ecosystem Commands: {ecosystem_commands}\n")
    
    # Calculate average line count
    if all_line_counts:
        complexity_summary['Line Count Statistics']['Average Lines'] = sum(all_line_counts) / len(all_line_counts)
    
    return complexity_summary

# Example usage
if __name__ == "__main__":
    # Example of how to use the script
    import sys
    
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        results = batch_analyze_scripts(directory)
        
        # Pretty print the results
        import json
        print(json.dumps(results, indent=2))
    else:
        print("Please provide a directory path")

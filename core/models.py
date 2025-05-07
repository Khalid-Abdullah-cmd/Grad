from django.db import models



class University(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    
    def __str__(self):
        return self.name
    
    
    def program_count(self):
        return sum(faculty.programs.count() for faculty in self.faculties.all())
    
    
class Faculty(models.Model):
    name = models.CharField(max_length=255, unique=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='faculties')
    
    
    def __str__(self):
        return self.name
    
class Program(models.Model):
    name = models.CharField(max_length=255, unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='programs')
    content = models.TextField()
    description = models.TextField()
    link = models.URLField()
    
    def __str__(self):
        return self.name        
    
class Job(models.Model):
    name = models.CharField(max_length=255, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='jobs')
    
    
    def __str__(self):
        return self.name    